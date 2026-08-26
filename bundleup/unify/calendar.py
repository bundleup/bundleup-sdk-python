from typing import Any, Dict, cast

from .base import Base
from .types import EventsResponse


class Calendar(Base):
    def events(self, params: Dict[str, Any]) -> EventsResponse:
        """
        List calendar events

        ``params`` must carry ``starts_after`` and ``starts_before`` (ISO
        8601) — the endpoint refuses an unbounded listing.
        """
        if not params or not params.get("starts_after") or not params.get("starts_before"):
            raise ValueError("starts_after and starts_before are required to fetch events.")

        url = self._build_url("calendar/events")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch calendar/events: {response.status_code}")

        return cast(EventsResponse, response.json())
