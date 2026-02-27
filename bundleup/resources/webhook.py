from .base import Base


class Webhook(Base):
    @property
    def _resource_name(self):
        return "webhooks"

    def list(self, params: dict = None):
        """
        List all webhooks
        """
        return super()._list(params)

    def create(self, body: dict):
        """
        Create a new webhook
        """
        return super()._create(body)

    def retrieve(self, id: str):
        """
        Retrieve a webhook by ID
        """
        return super()._retrieve(id)

    def update(self, id: str, body: dict):
        """
        Update a webhook by ID
        """
        return super()._update(id, body)

    def delete(self, id: str):
        """
        Delete a webhook by ID
        """
        return super()._delete(id)
