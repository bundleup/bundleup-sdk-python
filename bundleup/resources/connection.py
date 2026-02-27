from .base import Base


class Connection(Base):
    @property
    def _resource_name(self):
        return "connections"

    def list(self, params: dict = None):
        """
        List all connections
        """
        return super()._list(params)

    def retrieve(self, id: str):
        """
        Retrieve a connection by ID.
        """
        return super()._retrieve(id)

    def delete(self, id: str):
        """
        Delete a connection by ID.
        """
        return super()._delete(id)
