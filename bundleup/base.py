"""Base class for BundleUp API resources."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, TypeVar
import requests

from .utils import validate_non_empty_string, validate_dict
from .exceptions import APIError, AuthenticationError, NotFoundError, RateLimitError


T = TypeVar('T', bound=Dict[str, Any])


class Base(ABC, Generic[T]):
    """Base class for API resources with CRUD operations."""
    
    base_url: str = "https://api.bundleup.io"
    version: str = "v1"
    
    def __init__(self, api_key: str, session: requests.Session = None):
        """
        Initialize the base resource.
        
        Args:
            api_key: The BundleUp API key
            session: Optional requests session for connection pooling
            
        Raises:
            ValidationError: If api_key is not a valid non-empty string
        """
        validate_non_empty_string(api_key, "api_key")
        self._api_key = api_key
        self._session = session or requests.Session()
    
    @property
    @abstractmethod
    def _namespace(self) -> str:
        """
        Get the API namespace for this resource.
        
        Returns:
            The namespace string (e.g., 'connections', 'integrations')
        """
        pass
    
    @property
    def _headers(self) -> Dict[str, str]:
        """
        Get the headers for API requests.
        
        Returns:
            Dictionary of HTTP headers
        """
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
    
    def _build_url(self, path: str = "") -> str:
        """
        Build the full API URL.
        
        Args:
            path: Optional path to append (e.g., resource ID)
            
        Returns:
            The complete API URL
        """
        url = f"{self.base_url}/{self.version}/{self._namespace}"
        if path:
            url = f"{url}/{path}"
        return url
    
    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle API response and raise appropriate exceptions.
        
        Args:
            response: The response object from requests
            
        Returns:
            Parsed JSON response
            
        Raises:
            AuthenticationError: For 401 status codes
            NotFoundError: For 404 status codes
            RateLimitError: For 429 status codes
            APIError: For other error status codes
        """
        try:
            response.raise_for_status()
            return response.json() if response.text else None
        except requests.exceptions.HTTPError as e:
            status_code = response.status_code
            try:
                error_body = response.text
            except:
                error_body = None
            
            if status_code == 401:
                raise AuthenticationError(
                    f"Authentication failed for {self._namespace}",
                    status_code=status_code,
                    response_body=error_body
                )
            elif status_code == 404:
                raise NotFoundError(
                    f"Resource not found in {self._namespace}",
                    status_code=status_code,
                    response_body=error_body
                )
            elif status_code == 429:
                raise RateLimitError(
                    f"Rate limit exceeded for {self._namespace}",
                    status_code=status_code,
                    response_body=error_body
                )
            else:
                raise APIError(
                    f"API request failed for {self._namespace}: {str(e)}",
                    status_code=status_code,
                    response_body=error_body
                )
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed for {self._namespace}: {str(e)}")
    
    def list(self, **params) -> List[T]:
        """
        List all resources.
        
        Args:
            **params: Optional query parameters
        
        Returns:
            List of resources
            
        Raises:
            APIError: If the API request fails
        """
        url = self._build_url()
        response = self._session.get(url, headers=self._headers, params=params)
        return self._handle_response(response)
    
    def create(self, data: T) -> T:
        """
        Create a new resource.
        
        Args:
            data: The resource data
            
        Returns:
            The created resource
            
        Raises:
            ValidationError: If data is not a dictionary
            APIError: If the API request fails
        """
        validate_dict(data, "data")
        url = self._build_url()
        response = self._session.post(url, json=data, headers=self._headers)
        return self._handle_response(response)
    
    def retrieve(self, id: str) -> T:
        """
        Retrieve a specific resource by ID.
        
        Args:
            id: The resource ID
            
        Returns:
            The resource
            
        Raises:
            ValidationError: If id is not a valid non-empty string
            APIError: If the API request fails
        """
        validate_non_empty_string(id, "id")
        url = self._build_url(id)
        response = self._session.get(url, headers=self._headers)
        return self._handle_response(response)
    
    def update(self, id: str, data: T) -> T:
        """
        Update a resource.
        
        Args:
            id: The resource ID
            data: The updated resource data
            
        Returns:
            The updated resource
            
        Raises:
            ValidationError: If id or data are invalid
            APIError: If the API request fails
        """
        validate_non_empty_string(id, "id")
        validate_dict(data, "data")
        url = self._build_url(id)
        response = self._session.patch(url, json=data, headers=self._headers)
        return self._handle_response(response)
    
    def delete(self, id: str) -> None:
        """
        Delete a resource.
        
        Args:
            id: The resource ID
            
        Raises:
            ValidationError: If id is not a valid non-empty string
            APIError: If the API request fails
        """
        validate_non_empty_string(id, "id")
        url = self._build_url(id)
        response = self._session.delete(url, headers=self._headers)
        self._handle_response(response)
    
    def __repr__(self) -> str:
        """Return a string representation of the resource."""
        return f"{self.__class__.__name__}(namespace='{self._namespace}')"
