from .chat import Chat
from .git import Git
from .ticketing import Ticketing
from .crm import CRM
from .drive import Drive
from .mcp import MCP


class Unify:
    def __init__(self, api_key: str, connection_id: str):
        # Initialize
        self.chat = Chat(api_key, connection_id)
        self.git = Git(api_key, connection_id)
        self.ticketing = Ticketing(api_key, connection_id)
        self.crm = CRM(api_key, connection_id)
        self.drive = Drive(api_key, connection_id)
        self.mcp = MCP(api_key, connection_id)
