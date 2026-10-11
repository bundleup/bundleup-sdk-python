from typing import Any, Dict, Optional, cast
from urllib.parse import quote

from .base import Base
from .types import TicketResponse, TicketsResponse


class Helpdesk(Base):
    def tickets(self, params: Optional[Dict[str, Any]] = None) -> TicketsResponse:
        """
        List support tickets
        """
        url = self._build_url("helpdesk/tickets")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch helpdesk/tickets: {response.status_code}")

        return cast(TicketsResponse, response.json())

    def ticket(self, ticket_id: str, params: Optional[Dict[str, Any]] = None) -> TicketResponse:
        """
        Get a single support ticket by ID (a `sys_id` on ServiceNow)
        """
        if not ticket_id:
            raise ValueError("ticket_id is required to fetch a ticket.")

        endpoint = f"helpdesk/tickets/{quote(str(ticket_id), safe='')}"
        url = self._build_url(endpoint)
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(TicketResponse, response.json())
