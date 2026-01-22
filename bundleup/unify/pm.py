"""BundleUp Unify Project Management API."""

from typing import Optional
from .base import UnifyBase, Params, Response


class PM(UnifyBase):
    """Project Management unify methods for standardized PM operations."""
    
    def issues(self, params: Optional[Params] = None) -> Response:
        """
        Get unified issues.
        
        Args:
            params: Optional query parameters (limit, after, include_raw)
            
        Returns:
            Unified response with issues
            
        Raises:
            RuntimeError: If the request fails
        """
        return self._request("/pm/issues", params)
