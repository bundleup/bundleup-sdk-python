from typing import Any, Dict, Optional

from .chat import Chat
from .git import Git
from .ticketing import Ticketing
from .crm import CRM
from .drive import Drive
from .mcp import MCP
from .me import Me
from .types import MeResponse


class Unify:
    def __init__(self, api_key: str, connection_id: str):
        # Initialize
        self.chat = Chat(api_key, connection_id)
        self.git = Git(api_key, connection_id)
        self.ticketing = Ticketing(api_key, connection_id)
        self.crm = CRM(api_key, connection_id)
        self.drive = Drive(api_key, connection_id)
        self.mcp = MCP(api_key, connection_id)
        self._me = Me(api_key, connection_id)

    def me(self, params: Optional[Dict[str, Any]] = None) -> MeResponse:
        """
        Get the account this connection is authenticated as.

        `me` is the one unified method every provider implements, so it hangs
        off the Unify client directly instead of a vertical namespace.
        """
        return self._me.get(params)
