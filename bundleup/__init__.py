from .mcp import MCP, MCPClient
from .proxy import Proxy
from .unify import Unify

# Resources
from .resources.connection import Connection
from .resources.integration import Integration
from .resources.webhook import Webhook


class BundleUp:
    def __init__(self, api_key: str):
        if api_key is None:
            raise Exception("API key is required to initialize BundleUp SDK.")

        self._api_key = api_key

        # Initialize resource instances
        self.connection = Connection(api_key)
        self.integration = Integration(api_key)
        self.webhook = Webhook(api_key)

    def proxy(self, connection_id: str) -> Proxy:
        if connection_id is None:
            raise Exception("Connection ID is required to create a Proxy client.")

        return Proxy(self._api_key, connection_id)

    def unify(self, connection_id: str) -> Unify:
        if connection_id is None:
            raise Exception("Connection ID is required to create a Unify client.")

        return Unify(self._api_key, connection_id)

    def mcp(self, connection_id: str) -> MCP:
        if connection_id is None:
            raise Exception("Connection ID is required to create an MCP client.")

        return MCP(self._api_key, connection_id)


__all__ = ["BundleUp", "MCP", "MCPClient", "Proxy", "Unify"]
