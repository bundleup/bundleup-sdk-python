"""BundleUp Connections resource."""

from typing import Any, Dict, TypedDict
from .base import Base


class Connection(TypedDict, total=False):
    """Connection resource type."""
    id: str
    name: str
    integration_id: str
    status: str
    created_at: str
    updated_at: str


class Connections(Base[Connection]):
    """Connections resource class for managing connection resources."""
    
    @property
    def _namespace(self) -> str:
        """Get the API namespace for connections."""
        return "connections"
