"""BundleUp Unify Git API."""

from typing import Optional
from .base import UnifyBase, Params, Response


class Git(UnifyBase):
    """Git unify methods for standardized git operations."""
    
    def repos(self, params: Optional[Params] = None) -> Response:
        """
        Get unified git repositories.
        
        Args:
            params: Optional query parameters (limit, after, include_raw)
            
        Returns:
            Unified response with repositories
            
        Raises:
            RuntimeError: If the request fails
        """
        return self._request("/git/repos", params)
    
    def pulls(self, params: Optional[Params] = None) -> Response:
        """
        Get unified pull requests.
        
        Args:
            params: Optional query parameters (limit, after, include_raw)
            
        Returns:
            Unified response with pull requests
            
        Raises:
            RuntimeError: If the request fails
        """
        return self._request("/git/pulls", params)
    
    def tags(self, params: Optional[Params] = None) -> Response:
        """
        Get unified git tags.
        
        Args:
            params: Optional query parameters (limit, after, include_raw)
            
        Returns:
            Unified response with tags
            
        Raises:
            RuntimeError: If the request fails
        """
        return self._request("/git/tags", params)
    
    def releases(self, params: Optional[Params] = None) -> Response:
        """
        Get unified releases.
        
        Args:
            params: Optional query parameters (limit, after, include_raw)
            
        Returns:
            Unified response with releases
            
        Raises:
            RuntimeError: If the request fails
        """
        return self._request("/git/releases", params)
