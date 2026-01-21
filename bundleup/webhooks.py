"""BundleUp Webhooks resource."""

from typing import Any, Dict, List, TypedDict
from .base import Base


class Webhook(TypedDict, total=False):
    """Webhook resource type."""
    id: str
    url: str
    events: List[str]
    secret: str
    active: bool
    created_at: str
    updated_at: str


class Webhooks(Base[Webhook]):
    """Webhooks resource class for managing webhook resources."""
    
    @property
    def _namespace(self) -> str:
        """Get the API namespace for webhooks."""
        return "webhooks"
