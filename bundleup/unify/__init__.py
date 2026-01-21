"""BundleUp Unify API module."""

from .base import UnifyBase, Params, Response, Metadata
from .chat import Chat
from .git import Git
from .pm import PM
from ..utils import validate_non_empty_string


class Unify:
    """Unify API client with access to all unify resources."""
    
    def __init__(self, api_key: str, connection_id: str):
        """
        Initialize the Unify client.
        
        Args:
            api_key: The BundleUp API key
            connection_id: The connection ID
            
        Raises:
            ValueError: If api_key or connection_id are invalid
        """
        validate_non_empty_string(api_key, "api_key")
        validate_non_empty_string(connection_id, "connection_id")
        self._api_key = api_key
        self._connection_id = connection_id
    
    @property
    def chat(self) -> Chat:
        """Get the Chat unify resource."""
        return Chat(self._api_key, self._connection_id)
    
    @property
    def git(self) -> Git:
        """Get the Git unify resource."""
        return Git(self._api_key, self._connection_id)
    
    @property
    def pm(self) -> PM:
        """Get the PM (Project Management) unify resource."""
        return PM(self._api_key, self._connection_id)


__all__ = [
    "Unify",
    "UnifyBase",
    "Params",
    "Response",
    "Metadata",
    "Chat",
    "Git",
    "PM",
]
