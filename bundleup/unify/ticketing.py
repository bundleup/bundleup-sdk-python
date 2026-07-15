from .base import Base


class Ticketing(Base):
    def tickets(self, params: dict = None):
        """
        List ticketing tickets
        """
        url = self._build_url("ticketing/tickets")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch ticketing/tickets: {response.status_code}")

        return response.json()
