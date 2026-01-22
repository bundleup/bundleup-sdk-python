"""BundleUp Unify Chat API."""

from typing import Optional
from .base import UnifyBase, Params, Response


class Chat(UnifyBase):
    """Chat unify methods for standardized chat operations."""
    
    def channels(self, params: Optional[Params] = None) -> Response:
        """
        Get unified chat channels.
        
        Args:
            params: Optional query parameters (limit, after, include_raw)
            
        Returns:
            Unified response with chat channels
            
        Raises:
            RuntimeError: If the request fails
        """
        return self._request("/chat/channels", params)
