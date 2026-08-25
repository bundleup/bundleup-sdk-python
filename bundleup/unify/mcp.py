from typing import Any, Dict, List, Optional

from ..mcp import CREDENTIAL_SEPARATOR, MCPClient


class MCP:
    """
    The Unified MCP server.

    Same protocol and headers as Proxy MCP, but the tools are BundleUp's
    normalized ones rather than the provider's. Tools only — Unified MCP
    exposes no resources or prompts.

    The server is stateless and POST-only, so there is no session to close.
    """

    base_url: str = "https://unify.bundleup.io/v1/mcp"

    def __init__(self, api_key: str, connection_id: str):
        self._api_key = api_key
        self._connection_id = connection_id
        self._client = MCPClient(self.base_url, api_key, connection_id)

    def hosted(self) -> Dict[str, str]:
        """
        The URL and a single bearer token carrying both the API key and the
        connection, for model-hosted MCP clients that cannot set headers.
        """
        return {
            "url": self.base_url,
            "token": f"{self._api_key}{CREDENTIAL_SEPARATOR}{self._connection_id}",
        }

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List the available unified tools.
        """
        return self._client.list_tools()

    def call_tool(self, name: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Call a unified tool with optional arguments.
        """
        if not name:
            raise ValueError("Tool name is required to call a tool.")

        return self._client.call_tool(name, args)
