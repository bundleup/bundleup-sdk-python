"""BundleUp Proxy API client."""

from typing import Any, Dict, Optional
import requests

from .utils import validate_non_empty_string


class Proxy:
    """Proxy class for making direct API calls to connected services."""
    
    base_url: str = "https://proxy.bundleup.io"
    
    def __init__(self, api_key: str, connection_id: str):
        """
        Initialize the Proxy client.
        
        Args:
            api_key: The BundleUp API key
            connection_id: The connection ID to proxy requests through
            
        Raises:
            ValueError: If api_key or connection_id are invalid
        """
        validate_non_empty_string(api_key, "api_key")
        validate_non_empty_string(connection_id, "connection_id")
        self._api_key = api_key
        self._connection_id = connection_id
    
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
    
    def get(self, path: str, headers: Optional[Dict[str, str]] = None) -> Any:
        """
        Make a GET request through the proxy.
        
        Args:
            path: The API path
            headers: Optional additional headers
            
        Returns:
            The response data
            
        Raises:
            ValueError: If path is invalid
            RuntimeError: If the request fails
        """
        validate_non_empty_string(path, "path")
        url = self._build_url(path)
        try:
            response = requests.get(url, headers=self._get_headers(headers))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Proxy GET request failed: {str(e)}")
    
    def post(self, path: str, data: Optional[Dict[str, Any]] = None, 
             headers: Optional[Dict[str, str]] = None) -> Any:
        """
        Make a POST request through the proxy.
        
        Args:
            path: The API path
            data: Optional request body data
            headers: Optional additional headers
            
        Returns:
            The response data
            
        Raises:
            ValueError: If path is invalid
            RuntimeError: If the request fails
        """
        validate_non_empty_string(path, "path")
        url = self._build_url(path)
        try:
            response = requests.post(url, json=data, headers=self._get_headers(headers))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Proxy POST request failed: {str(e)}")
    
    def put(self, path: str, data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> Any:
        """
        Make a PUT request through the proxy.
        
        Args:
            path: The API path
            data: Optional request body data
            headers: Optional additional headers
            
        Returns:
            The response data
            
        Raises:
            ValueError: If path is invalid
            RuntimeError: If the request fails
        """
        validate_non_empty_string(path, "path")
        url = self._build_url(path)
        try:
            response = requests.put(url, json=data, headers=self._get_headers(headers))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Proxy PUT request failed: {str(e)}")
    
    def patch(self, path: str, data: Optional[Dict[str, Any]] = None,
              headers: Optional[Dict[str, str]] = None) -> Any:
        """
        Make a PATCH request through the proxy.
        
        Args:
            path: The API path
            data: Optional request body data
            headers: Optional additional headers
            
        Returns:
            The response data
            
        Raises:
            ValueError: If path is invalid
            RuntimeError: If the request fails
        """
        validate_non_empty_string(path, "path")
        url = self._build_url(path)
        try:
            response = requests.patch(url, json=data, headers=self._get_headers(headers))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Proxy PATCH request failed: {str(e)}")
    
    def delete(self, path: str, headers: Optional[Dict[str, str]] = None) -> Any:
        """
        Make a DELETE request through the proxy.
        
        Args:
            path: The API path
            headers: Optional additional headers
            
        Returns:
            The response data
            
        Raises:
            ValueError: If path is invalid
            RuntimeError: If the request fails
        """
        validate_non_empty_string(path, "path")
        url = self._build_url(path)
        try:
            response = requests.delete(url, headers=self._get_headers(headers))
            response.raise_for_status()
            # DELETE may return empty response
            if response.text:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Proxy DELETE request failed: {str(e)}")
