from .base import Base


class Integration(Base):
    @property
    def _resource_name(self):
        return "integrations"

    def list(self, params: dict = None):
        """
        List all integrations
        """
        return super()._list(params)

    def retrieve(self, id):
        """
        Retrieve an integration by ID.
        """
        return super()._retrieve(id)
