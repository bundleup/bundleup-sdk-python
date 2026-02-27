from .base import Base


class Chat(Base):
    def channels(self, params: dict = None):
        """
        List chat channels
        """
        url = self._build_url("chat/channels")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch chat/channels: {response.status_code}")

        return response.json()
