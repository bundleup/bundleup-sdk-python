"""Custom exceptions for the BundleUp SDK."""


class BundleUpError(Exception):
    """Base exception for all BundleUp SDK errors."""
    
    pass


class ValidationError(BundleUpError):
    """Raised when input validation fails."""
    
    pass


class APIError(BundleUpError):
    """Raised when an API request fails."""
    
    def __init__(self, message: str, status_code: int = None, response_body: str = None):
        """
        Initialize the API error.
        
        Args:
            message: Error message
            status_code: HTTP status code if available
            response_body: Response body if available
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body
    
    def __str__(self) -> str:
        """Return a formatted error message."""
        parts = [super().__str__()]
        if self.status_code:
            parts.append(f"Status code: {self.status_code}")
        if self.response_body:
            parts.append(f"Response: {self.response_body}")
        return " | ".join(parts)


class AuthenticationError(APIError):
    """Raised when authentication fails."""
    
    pass


class NotFoundError(APIError):
    """Raised when a resource is not found."""
    
    pass


class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""
    
    pass
