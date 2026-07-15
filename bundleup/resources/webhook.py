from typing import Any, Dict, Optional

from .base import Base


class Webhook(Base):
    @property
    def _resource_name(self) -> str:
        return "webhooks"

    def list(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List all webhooks
        """
        return super()._list(params)

    def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new webhook
        """
        return super()._create(body)

    def retrieve(self, id: str) -> Dict[str, Any]:
        """
        Retrieve a webhook by ID
        """
        return super()._retrieve(id)

    def update(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a webhook by ID
        """
        return super()._update(id, body)

    def delete(self, id: str) -> None:
        """
        Delete a webhook by ID
        """
        return super()._delete(id)
