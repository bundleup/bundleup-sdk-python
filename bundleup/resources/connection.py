from typing import Any, Dict, Optional

from .base import Base


class Connection(Base):
    @property
    def _resource_name(self) -> str:
        return "connections"

    def list(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List all connections
        """
        return super()._list(params)

    def retrieve(self, id: str) -> Dict[str, Any]:
        """
        Retrieve a connection by ID.
        """
        return super()._retrieve(id)

    def delete(self, id: str) -> None:
        """
        Delete a connection by ID.
        """
        return super()._delete(id)
