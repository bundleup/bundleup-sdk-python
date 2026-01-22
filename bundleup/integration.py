"""BundleUp Integrations resource."""

from typing import Any, Dict, TypedDict
from .base import Base


class Integration(TypedDict, total=False):
    """Integration resource type."""
    id: str
    name: str
    slug: str
    category: str
    logo_url: str
    description: str
    auth_type: str
    created_at: str
    updated_at: str


class Integrations(Base[Integration]):
    """Integrations resource class for managing integration resources."""
    
    @property
    def _namespace(self) -> str:
        """Get the API namespace for integrations."""
        return "integrations"
