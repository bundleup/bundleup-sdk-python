from typing import Any, Dict, Optional, Union

import requests

# Separates the API key from an appended connection ID. Safe to split on:
# API keys are alphanumeric and connection IDs are cuids, so neither can
# contain a period.
CREDENTIAL_SEPARATOR = "."


class MCP:
    """
    A connection's MCP server.

    BundleUp does not ship an MCP client. Hand ``transport()`` or ``hosted()``
    to the client you already use — the official ``mcp`` package, OpenAI
    Agents SDK, LangChain — or drive the protocol yourself with ``post`` and
    ``delete``, which return the raw response the way
    :class:`~bundleup.proxy.Proxy` does.
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
