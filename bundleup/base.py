"""Base class for BundleUp API resources."""

from abc import ABC
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
import requests

from .utils import validate_non_empty_string, validate_dict


T = TypeVar('T', bound=Dict[str, Any])


class Base(ABC, Generic[T]):
    """Base class for API resources with CRUD operations."""
    
    base_url: str = "https://api.bundleup.io"
    version: str = "v1"
    
    def __init__(self, api_key: str):
        """
        Initialize the base resource.
        
        Args:
            api_key: The BundleUp API key
            
        Raises:
            ValueError: If api_key is not a valid non-empty string
        """
        validate_non_empty_string(api_key, "api_key")
        self._api_key = api_key
    
    @property
    def _namespace(self) -> str:
        """
        Get the API namespace for this resource.
        
        Returns:
            The namespace string (e.g., 'connections', 'integrations')
            
        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement _namespace property")
    
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
    
    def list(self) -> List[T]:
        """
        List all resources.
        
        Returns:
            List of resources
            
        Raises:
            RuntimeError: If the API request fails
        """
        url = self._build_url()
        try:
            response = requests.get(url, headers=self._headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to list {self._namespace}: {str(e)}")
    
    def create(self, data: T) -> T:
        """
        Create a new resource.
        
        Args:
            data: The resource data
            
        Returns:
            The created resource
            
        Raises:
            ValueError: If data is not a dictionary
            RuntimeError: If the API request fails
        """
        validate_dict(data, "data")
        url = self._build_url()
        try:
            response = requests.post(url, json=data, headers=self._headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to create {self._namespace}: {str(e)}")
    
    def retrieve(self, id: str) -> T:
        """
        Retrieve a specific resource by ID.
        
        Args:
            id: The resource ID
            
        Returns:
            The resource
            
        Raises:
            ValueError: If id is not a valid non-empty string
            RuntimeError: If the API request fails
        """
        validate_non_empty_string(id, "id")
        url = self._build_url(id)
        try:
            response = requests.get(url, headers=self._headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to retrieve {self._namespace} {id}: {str(e)}")
    
    def update(self, id: str, data: T) -> T:
        """
        Update a resource.
        
        Args:
            id: The resource ID
            data: The updated resource data
            
        Returns:
            The updated resource
            
        Raises:
            ValueError: If id or data are invalid
            RuntimeError: If the API request fails
        """
        validate_non_empty_string(id, "id")
        validate_dict(data, "data")
        url = self._build_url(id)
        try:
            response = requests.patch(url, json=data, headers=self._headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to update {self._namespace} {id}: {str(e)}")
    
    def delete(self, id: str) -> None:
        """
        Delete a resource.
        
        Args:
            id: The resource ID
            
        Raises:
            ValueError: If id is not a valid non-empty string
            RuntimeError: If the API request fails
        """
        validate_non_empty_string(id, "id")
        url = self._build_url(id)
        try:
            response = requests.delete(url, headers=self._headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to delete {self._namespace} {id}: {str(e)}")
