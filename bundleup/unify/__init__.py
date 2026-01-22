"""BundleUp Unify API module."""

from typing import Optional
import requests

from .base import UnifyBase, Params, Response, Metadata
from .chat import Chat
from .git import Git
from .pm import PM
from ..utils import validate_non_empty_string


class Unify:
    """Unify API client with access to all unify resources."""
    
    def __init__(self, api_key: str, connection_id: str, session: Optional[requests.Session] = None):
        """
        Initialize the Unify client.
        
        Args:
            api_key: The BundleUp API key
            connection_id: The connection ID
            session: Optional requests session for connection pooling
            
        Raises:
            ValidationError: If api_key or connection_id are invalid
        """
        validate_non_empty_string(api_key, "api_key")
        validate_non_empty_string(connection_id, "connection_id")
        self._api_key = api_key
        self._connection_id = connection_id
        self._session = session or requests.Session()
    
    @property
    def chat(self) -> Chat:
        """Get the Chat unify resource."""
        return Chat(self._api_key, self._connection_id, self._session)
    
    @property
    def git(self) -> Git:
        """Get the Git unify resource."""
        return Git(self._api_key, self._connection_id, self._session)
    
    @property
    def pm(self) -> PM:
        """Get the PM (Project Management) unify resource."""
        return PM(self._api_key, self._connection_id, self._session)
    
    def __repr__(self) -> str:
        """Return a string representation of the Unify client."""
        return f"Unify(connection_id='{self._connection_id}')"


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
