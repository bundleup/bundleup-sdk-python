import json as jsonlib
from typing import Any, Dict, List, Optional, Union

import requests

PROTOCOL_VERSION = "2025-06-18"
CLIENT_NAME = "bundleup-sdk"
CLIENT_VERSION = "0.2.0"

# Separates the API key from an appended connection ID. Safe to split on:
# API keys are alphanumeric and connection IDs are cuids, so neither can
# contain a period.
CREDENTIAL_SEPARATOR = "."


class MCP:
    """
    Transport for a connection's MCP server.

    ``post`` and ``delete`` return the raw response untouched, the way
    :class:`~bundleup.proxy.Proxy` does. Use ``connect()`` for a managed
    session that handles the handshake and decoding for you.
    """

    base_url: str = "https://mcp.bundleup.io"

    def __init__(self, api_key: str, connection_id: str):
        self._api_key = api_key
        self._connection_id = connection_id

    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {self._api_key}",
            "BU-Connection-Id": self._connection_id,
        }

    def transport(self) -> Dict[str, Any]:
        """
        The URL and headers for this connection's MCP server, for an MCP
        client library running in your own process.
        """
        return {"url": self.base_url, "headers": self._headers}

    def hosted(self) -> Dict[str, str]:
        """
        The URL and a single bearer token carrying both the API key and the
        connection.

        For model-hosted MCP — OpenAI's Responses API, Anthropic's Messages
        API — where the model provider connects to the server itself and
        accepts one credential with no way to add a ``BU-Connection-Id``
        header. Note this hands your API key to the model provider.
        """
        return {
            "url": self.base_url,
            "token": f"{self._api_key}{CREDENTIAL_SEPARATOR}{self._connection_id}",
        }

    def post(
        self,
        body: Union[Dict[str, Any], str, bytes],
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """
        Send a JSON-RPC message and return the raw response.

        Pass ``Mcp-Session-Id`` in ``headers`` to stay on an existing session.
        """
        request = requests.Session()
        request.headers.update(self._headers)

        if headers:
            request.headers.update(headers)

        if isinstance(body, (str, bytes)):
            return request.post(self.base_url, data=body)

        return request.post(self.base_url, json=body)

    def delete(self, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        End an MCP session. Pass the session's ``Mcp-Session-Id`` in ``headers``.
        """
        request = requests.Session()
        request.headers.update(self._headers)

        if headers:
            request.headers.update(headers)

        return request.delete(self.base_url)

    def connect(self) -> "MCPClient":
        """
        Open a managed MCP session for this connection.

        Handles the handshake, session ID and response decoding, and exposes
        the provider's tools, resources and prompts.
        """
        return MCPClient(self.base_url, self._api_key, self._connection_id)


class MCPClient:
    """
    A connected MCP session.

    Tools, resources and prompts are defined by the provider — BundleUp does
    not rename or normalize them.
    """

    def __init__(self, base_url: str, api_key: str, connection_id: str):
        self._base_url = base_url
        self._api_key = api_key
        self._connection_id = connection_id
        self._session_id: Optional[str] = None
        self._is_connected = False
        self._last_id = 0

    @property
    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {self._api_key}",
            "BU-Connection-Id": self._connection_id,
        }

        if self._session_id:
            headers["Mcp-Session-Id"] = self._session_id

        return headers

    def _post(self, payload: Dict[str, Any]) -> requests.Response:
        request = requests.Session()
        request.headers.update(self._headers)

        response = request.post(self._base_url, json=payload)

        session_id = response.headers.get("mcp-session-id")

        if session_id:
            self._session_id = session_id

        if not response.ok:
            message = f"MCP request failed with status {response.status_code}."

            try:
                # BundleUp rejections carry code and message; provider errors
                # are not guaranteed to be JSON.
                parsed = response.json()

                if isinstance(parsed, dict) and parsed.get("message"):
                    code = parsed.get("code")
                    message = f"{parsed['message']} ({code})" if code else str(parsed["message"])
            except ValueError:
                pass

            raise Exception(message)

        return response

    @staticmethod
    def _parse(response: requests.Response, message_id: int) -> Optional[Dict[str, Any]]:
        """
        Pull the message matching ``message_id`` out of the response. Providers
        may answer a plain request/response over ``text/event-stream``.
        """
        body = response.text

        if not body:
            return None

        if "text/event-stream" not in response.headers.get("content-type", ""):
            return dict(jsonlib.loads(body))

        for event in body.replace("\r\n", "\n").split("\n\n"):
            lines = [line for line in event.split("\n") if line.startswith("data:")]
            data = "\n".join(line[len("data:") :].strip() for line in lines)

            if not data:
                continue

            message = jsonlib.loads(data)

            # Skip server notifications interleaved on the stream.
            if isinstance(message, dict) and message.get("id") == message_id:
                return dict(message)

        return None

    def _send(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._last_id += 1
        message_id = self._last_id

        payload: Dict[str, Any] = {"jsonrpc": "2.0", "id": message_id, "method": method}

        if params is not None:
            payload["params"] = params

        response = self._post(payload)
        message = self._parse(response, message_id)

        if message is None:
            raise Exception(f"No response received for {method}.")

        if message.get("error"):
            raise Exception(message["error"].get("message", f"{method} failed."))

        return dict(message.get("result") or {})

    def _connect(self) -> None:
        """
        Run the MCP handshake, once. Deferred until the first call.
        """
        if self._is_connected:
            return

        self._send(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": CLIENT_NAME, "version": CLIENT_VERSION},
            },
        )

        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

        self._is_connected = True

    def _paginate(self, method: str, key: str) -> List[Dict[str, Any]]:
        self._connect()

        items: List[Dict[str, Any]] = []
        cursor: Optional[str] = None

        while True:
            result = self._send(method, {"cursor": cursor} if cursor else None)

            items.extend(result.get(key) or [])
            cursor = result.get("nextCursor")

            if not cursor:
                break

        return items

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List the provider's tools, following pagination to the end.
        """
        return self._paginate("tools/list", "tools")

    def call_tool(self, name: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Call a tool by name, with arguments matching its own input schema.
        """
        if not name:
            raise ValueError("Tool name is required to call a tool.")

        self._connect()

        return self._send("tools/call", {"name": name, "arguments": args or {}})

    def list_resources(self) -> List[Dict[str, Any]]:
        """
        List the provider's resources, following pagination to the end.
        """
        return self._paginate("resources/list", "resources")

    def read_resource(self, uri: str) -> Dict[str, Any]:
        """
        Read a resource by URI.
        """
        if not uri:
            raise ValueError("Resource URI is required to read a resource.")

        self._connect()

        return self._send("resources/read", {"uri": uri})

    def list_prompts(self) -> List[Dict[str, Any]]:
        """
        List the provider's prompts, following pagination to the end.
        """
        return self._paginate("prompts/list", "prompts")

    def get_prompt(self, name: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get a prompt by name.
        """
        if not name:
            raise ValueError("Prompt name is required to get a prompt.")

        self._connect()

        return self._send("prompts/get", {"name": name, "arguments": args or {}})

    def request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send any other JSON-RPC method on this session.
        """
        if not method:
            raise ValueError("Method is required to send a request.")

        self._connect()

        return self._send(method, params)

    def close(self) -> None:
        """
        End the session and reset local state.
        """
        if self._session_id:
            request = requests.Session()
            request.headers.update(self._headers)

            try:
                request.delete(self._base_url)
            except requests.RequestException:
                pass

        self._session_id = None
        self._is_connected = False
