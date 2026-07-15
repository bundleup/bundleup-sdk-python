from typing import Any, Dict, Optional, cast
from .base import Base
from .types import TicketsResponse

class Ticketing(Base):
    def tickets(self, params: Optional[Dict[str, Any]] = None) -> TicketsResponse:
        """
        List ticketing tickets
        """
        url = self._build_url("ticketing/tickets")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch ticketing/tickets: {response.status_code}")

        return cast(TicketsResponse, response.json())
