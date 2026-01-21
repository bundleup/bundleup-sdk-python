"""BundleUp Python SDK.

Official Python SDK for the BundleUp API.

Example:
    >>> from bundleup import BundleUp
    >>> client = BundleUp("your-api-key")
    >>> connections = client.connections.list()
"""

from .base import Base
from .connection import Connection, Connections
from .integration import Integration, Integrations
from .webhooks import Webhook, Webhooks
from .proxy import Proxy
from .unify import Unify
from .utils import validate_non_empty_string

__version__ = "0.1.0"


class BundleUp:
    """Main BundleUp SDK client."""
    
    def __init__(self, api_key: str):
        """
        Initialize the BundleUp client.
        
        Args:
            api_key: Your BundleUp API key
            
        Raises:
            ValueError: If api_key is not a valid non-empty string
            
        Example:
            >>> client = BundleUp("your-api-key")
        """
        validate_non_empty_string(api_key, "api_key")
        self._api_key = api_key
        
        # Initialize resource instances
        self._connections = Connections(api_key)
        self._integrations = Integrations(api_key)
        self._webhooks = Webhooks(api_key)
    
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
            ValueError: If connection_id is not a valid non-empty string
            
        Example:
            >>> proxy = client.proxy("connection-id")
            >>> data = proxy.get("/users")
        """
        return Proxy(self._api_key, connection_id)
    
    def unify(self, connection_id: str) -> Unify:
        """
        Create a Unify client for standardized API calls.
        
        Args:
            connection_id: The connection ID to use for unify requests
            
        Returns:
            Unify instance for the specified connection
            
        Raises:
            ValueError: If connection_id is not a valid non-empty string
            
        Example:
            >>> unify = client.unify("connection-id")
            >>> channels = unify.chat.channels()
            >>> repos = unify.git.repos()
        """
        return Unify(self._api_key, connection_id)


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
]
