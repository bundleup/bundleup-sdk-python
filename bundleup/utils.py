"""BundleUp Python SDK utilities."""

from typing import Any, Dict


def validate_non_empty_string(value: Any, param_name: str) -> None:
    """
    Validate that a value is a non-empty string.
    
    Args:
        value: The value to validate
        param_name: The parameter name for error messages
        
    Raises:
        ValueError: If the value is not a non-empty string
    """
    if not isinstance(value, str):
        raise ValueError(f"{param_name} must be a string")
    if not value.strip():
        raise ValueError(f"{param_name} cannot be empty")


def validate_dict(value: Any, param_name: str) -> None:
    """
    Validate that a value is a dictionary.
    
    Args:
        value: The value to validate
        param_name: The parameter name for error messages
        
    Raises:
        ValueError: If the value is not a dictionary
    """
    if not isinstance(value, dict):
        raise ValueError(f"{param_name} must be a dictionary")


def merge_headers(*headers: Dict[str, str]) -> Dict[str, str]:
    """
    Merge multiple header dictionaries.
    
    Args:
        *headers: Variable number of header dictionaries
        
    Returns:
        Merged dictionary of headers
    """
    result: Dict[str, str] = {}
    for header_dict in headers:
        result.update(header_dict)
    return result
