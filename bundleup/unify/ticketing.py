from typing import Any, Dict, Optional, cast
from urllib.parse import quote

from .base import Base
from .types import TicketResponse, TicketsResponse


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

    def ticket(self, ticket_id: str, params: Optional[Dict[str, Any]] = None) -> TicketResponse:
        """
        Get a single ticket by ID

        Not supported by Basecamp, whose API only serves a to-do underneath its
        project — an id on its own cannot address one.
        """
        if not ticket_id:
            raise ValueError("ticket_id is required to fetch a ticket.")

        endpoint = f"ticketing/tickets/{quote(str(ticket_id), safe='')}"
        url = self._build_url(endpoint)
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(TicketResponse, response.json())
