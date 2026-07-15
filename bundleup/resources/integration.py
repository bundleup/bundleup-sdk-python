from typing import Any, Dict, Optional

from .base import Base


class Integration(Base):
    @property
    def _resource_name(self) -> str:
        return "integrations"

    def list(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List all integrations
        """
        return super()._list(params)

    def retrieve(self, id: str) -> Dict[str, Any]:
        """
        Retrieve an integration by ID.
        """
        return super()._retrieve(id)
