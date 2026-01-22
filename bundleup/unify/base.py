"""Base class for BundleUp Unify API."""

from typing import Any, Dict, List, Optional, TypedDict
import requests

from ..utils import validate_non_empty_string
from ..exceptions import APIError


class Params(TypedDict, total=False):
    """Query parameters for Unify API requests."""
    limit: int
    after: str
    include_raw: bool


class Metadata(TypedDict, total=False):
    """Metadata for paginated responses."""
    has_more: bool
    next_cursor: Optional[str]


class Response(TypedDict):
    """Unify API response structure."""
    data: List[Dict[str, Any]]
    _raw: Optional[List[Dict[str, Any]]]
    metadata: Metadata


class UnifyBase:
    """Base class for Unify API resources."""
    
    base_url: str = "https://unify.bundleup.io"
    
    def __init__(self, api_key: str, connection_id: str, session: Optional[requests.Session] = None):
        """
        Initialize the Unify base client.
        
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
    def _headers(self) -> Dict[str, str]:
        """
        Get headers for Unify API requests.
        
        Returns:
            Dictionary of HTTP headers
        """
        return {
            "Authorization": f"Bearer {self._api_key}",
            "BU-Connection-Id": self._connection_id,
            "Content-Type": "application/json",
        }
    
    def _build_url(self, path: str) -> str:
        """
        Build the full Unify API URL.
        
        Args:
            path: The API path
            
        Returns:
            The complete Unify API URL
        """
        # Ensure path starts with /
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"
    
    def _request(self, path: str, params: Optional[Params] = None) -> Response:
        """
        Make a request to the Unify API.
        
        Args:
            path: The API path
            params: Optional query parameters
            
        Returns:
            The Unify API response
            
        Raises:
            APIError: If the request fails
        """
        url = self._build_url(path)
        query_params = {}
        
        if params:
            if "limit" in params:
                query_params["limit"] = params["limit"]
            if "after" in params:
                query_params["after"] = params["after"]
            if "include_raw" in params:
                query_params["include_raw"] = str(params["include_raw"]).lower()
        
        try:
            response = self._session.get(url, headers=self._headers, params=query_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            try:
                error_body = response.text if hasattr(response, 'text') else None
            except:
                error_body = None
            raise APIError(
                f"Unify API request failed: {str(e)}",
                status_code=response.status_code if hasattr(response, 'status_code') else None,
                response_body=error_body
            )
    
    def __repr__(self) -> str:
        """Return a string representation of the Unify base."""
        return f"{self.__class__.__name__}(connection_id='{self._connection_id}')"
