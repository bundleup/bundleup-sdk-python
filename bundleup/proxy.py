"""BundleUp Proxy API client."""

from typing import Any, Dict, Optional
import requests

from .utils import validate_non_empty_string
from .exceptions import APIError


class Proxy:
    """Proxy class for making direct API calls to connected services."""
    
    base_url: str = "https://proxy.bundleup.io"
    
    def __init__(self, api_key: str, connection_id: str, session: Optional[requests.Session] = None):
        """
        Initialize the Proxy client.
        
        Args:
            api_key: The BundleUp API key
            connection_id: The connection ID to proxy requests through
            session: Optional requests session for connection pooling
            
        Raises:
            ValidationError: If api_key or connection_id are invalid
        """
        validate_non_empty_string(api_key, "api_key")
        validate_non_empty_string(connection_id, "connection_id")
        self._api_key = api_key
        self._connection_id = connection_id
        self._session = session or requests.Session()
    
    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Get headers for proxy requests.
        
        Args:
            additional_headers: Optional additional headers to include
            
        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "BU-Connection-Id": self._connection_id,
            "Content-Type": "application/json",
        }
        if additional_headers:
            headers.update(additional_headers)
        return headers
    
    def _build_url(self, path: str) -> str:
        """
        Build the full proxy URL.
        
        Args:
            path: The API path
            
        Returns:
            The complete proxy URL
        """
        # Ensure path starts with /
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"
    
    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle proxy response and raise appropriate exceptions.
        
        Args:
            response: The response object from requests
            
        Returns:
            Parsed JSON response or None
            
        Raises:
            APIError: If the request fails
        """
        try:
            response.raise_for_status()
            return response.json() if response.text else None
        except requests.exceptions.RequestException as e:
            try:
                error_body = response.text
            except:
                error_body = None
            raise APIError(
                f"Proxy request failed: {str(e)}",
                status_code=response.status_code if hasattr(response, 'status_code') else None,
                response_body=error_body
            )
    
    def get(self, path: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Any:
        """
        Make a GET request through the proxy.
        
        Args:
            path: The API path
            headers: Optional additional headers
            **kwargs: Additional arguments passed to requests.get
            
        Returns:
            The response data
            
        Raises:
            ValidationError: If path is invalid
            APIError: If the request fails
        """
        validate_non_empty_string(path, "path")
        url = self._build_url(path)
        response = self._session.get(url, headers=self._get_headers(headers), **kwargs)
        return self._handle_response(response)
    
    def post(self, path: str, data: Optional[Dict[str, Any]] = None, 
             headers: Optional[Dict[str, str]] = None, **kwargs) -> Any:
        """
        Make a POST request through the proxy.
        
        Args:
            path: The API path
            data: Optional request body data
            headers: Optional additional headers
            **kwargs: Additional arguments passed to requests.post
            
        Returns:
            The response data
            
        Raises:
            ValidationError: If path is invalid
            APIError: If the request fails
        """
        validate_non_empty_string(path, "path")
        url = self._build_url(path)
        response = self._session.post(url, json=data, headers=self._get_headers(headers), **kwargs)
        return self._handle_response(response)
    
    def put(self, path: str, data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None, **kwargs) -> Any:
        """
        Make a PUT request through the proxy.
        
        Args:
            path: The API path
            data: Optional request body data
            headers: Optional additional headers
            **kwargs: Additional arguments passed to requests.put
            
        Returns:
            The response data
            
        Raises:
            ValidationError: If path is invalid
            APIError: If the request fails
        """
        validate_non_empty_string(path, "path")
        url = self._build_url(path)
        response = self._session.put(url, json=data, headers=self._get_headers(headers), **kwargs)
        return self._handle_response(response)
    
    def patch(self, path: str, data: Optional[Dict[str, Any]] = None,
              headers: Optional[Dict[str, str]] = None, **kwargs) -> Any:
        """
        Make a PATCH request through the proxy.
        
        Args:
            path: The API path
            data: Optional request body data
            headers: Optional additional headers
            **kwargs: Additional arguments passed to requests.patch
            
        Returns:
            The response data
            
        Raises:
            ValidationError: If path is invalid
            APIError: If the request fails
        """
        validate_non_empty_string(path, "path")
        url = self._build_url(path)
        response = self._session.patch(url, json=data, headers=self._get_headers(headers), **kwargs)
        return self._handle_response(response)
    
    def delete(self, path: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Any:
        """
        Make a DELETE request through the proxy.
        
        Args:
            path: The API path
            headers: Optional additional headers
            **kwargs: Additional arguments passed to requests.delete
            
        Returns:
            The response data or None
            
        Raises:
            ValidationError: If path is invalid
            APIError: If the request fails
        """
        validate_non_empty_string(path, "path")
        url = self._build_url(path)
        response = self._session.delete(url, headers=self._get_headers(headers), **kwargs)
        return self._handle_response(response)
    
    def __repr__(self) -> str:
        """Return a string representation of the proxy."""
        return f"Proxy(connection_id='{self._connection_id}')"
