"""BundleUp Python SDK.

Official Python SDK for the BundleUp API.

Example:
    >>> from bundleup import BundleUp
    >>> with BundleUp("your-api-key") as client:
    ...     connections = client.connections.list()
"""

from typing import Optional
import requests

from .base import Base
from .connection import Connection, Connections
from .integration import Integration, Integrations
from .webhooks import Webhook, Webhooks
from .proxy import Proxy
from .unify import Unify
from .utils import validate_non_empty_string
from .exceptions import BundleUpError, ValidationError, APIError

__version__ = "0.1.0"


class BundleUp:
    """Main BundleUp SDK client with context manager support."""
    
    def __init__(self, api_key: str, session: Optional[requests.Session] = None):
        """
        Initialize the BundleUp client.
        
        Args:
            api_key: Your BundleUp API key
            session: Optional requests session for connection pooling
            
        Raises:
            ValidationError: If api_key is not a valid non-empty string
            
        Example:
            >>> client = BundleUp("your-api-key")
            >>> # or use as context manager
            >>> with BundleUp("your-api-key") as client:
            ...     connections = client.connections.list()
        """
        validate_non_empty_string(api_key, "api_key")
        self._api_key = api_key
        self._session = session or requests.Session()
        self._owns_session = session is None
        
        # Initialize resource instances with shared session
        self._connections = Connections(api_key, self._session)
        self._integrations = Integrations(api_key, self._session)
        self._webhooks = Webhooks(api_key, self._session)
    
    def __enter__(self):
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and cleanup resources."""
        self.close()
        return False
    
    def close(self):
        """Close the underlying session if owned by this client."""
        if self._owns_session and self._session:
            self._session.close()
    
    @property
    def connections(self) -> Connections:
        """
        Access the Connections resource.
        
        Returns:
            Connections resource instance
            
        Example:
            >>> connections = client.connections.list()
        """
        return self._connections
    
    @property
    def integrations(self) -> Integrations:
        """
        Access the Integrations resource.
        
        Returns:
            Integrations resource instance
            
        Example:
            >>> integrations = client.integrations.list()
        """
        return self._integrations
    
    @property
    def webhooks(self) -> Webhooks:
        """
        Access the Webhooks resource.
        
        Returns:
            Webhooks resource instance
            
        Example:
            >>> webhooks = client.webhooks.list()
        """
        return self._webhooks
    
    def proxy(self, connection_id: str) -> Proxy:
        """
        Create a Proxy client for direct API calls to a connected service.
        
        Args:
            connection_id: The connection ID to proxy requests through
            
        Returns:
            Proxy instance for the specified connection
            
        Raises:
            ValidationError: If connection_id is not a valid non-empty string
            
        Example:
            >>> proxy = client.proxy("connection-id")
            >>> data = proxy.get("/users")
        """
        return Proxy(self._api_key, connection_id, self._session)
    
    def unify(self, connection_id: str) -> Unify:
        """
        Create a Unify client for standardized API calls.
        
        Args:
            connection_id: The connection ID to use for unify requests
            
        Returns:
            Unify instance for the specified connection
            
        Raises:
            ValidationError: If connection_id is not a valid non-empty string
            
        Example:
            >>> unify = client.unify("connection-id")
            >>> channels = unify.chat.channels()
            >>> repos = unify.git.repos()
        """
        return Unify(self._api_key, connection_id, self._session)
    
    def __repr__(self) -> str:
        """Return a string representation of the client."""
        return f"BundleUp(version='{__version__}')"


__all__ = [
    "BundleUp",
    "Base",
    "Connection",
    "Connections",
    "Integration",
    "Integrations",
    "Webhook",
    "Webhooks",
    "Proxy",
    "Unify",
    "BundleUpError",
    "ValidationError",
    "APIError",
]
