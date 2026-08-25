from typing import Any, Dict, Optional, cast

from .base import Base
from .types import MeResponse


class Me(Base):
    """
    `me` is the one unified method every provider implements, so the API mounts
    it at the root rather than under a vertical. It is exposed on the Unify
    client as `unify.me()` rather than as a namespace.
    """

    def get(self, params: Optional[Dict[str, Any]] = None) -> MeResponse:
        """
        Get the account the connection is authenticated as.

        Providers that authorize per workspace, portal, tenant or company return
        that account instead of a user, and fields the provider does not expose
        come back as None.
        """
        url = self._build_url("me")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch me: {response.status_code}")

        return cast(MeResponse, response.json())
