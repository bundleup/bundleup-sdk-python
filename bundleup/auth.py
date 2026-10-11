from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests


BASE_URL = "https://auth.bundleup.io"


def build_authorization_url(
    client_id: str,
    integration_id: str,
    redirect_uri: str,
    external_id: Optional[str] = None,
    state: Optional[str] = None,
) -> str:
    """Build the hosted authorization URL to send the end user to.

    Needs no API key: ``/authorize`` only takes the public client and
    integration ids, so this is safe to call where the key must not live.
    """
    if not client_id:
        raise ValueError("client_id is required")

    if not integration_id:
        raise ValueError("integration_id is required")

    if not redirect_uri:
        raise ValueError("redirect_uri is required")

    params = {
        "client_id": client_id,
        "integration_id": integration_id,
        "redirect_uri": redirect_uri,
    }

    if external_id:
        params["external_id"] = external_id

    if state:
        params["state"] = state

    return f"{BASE_URL}/authorize?{urlencode(params)}"


class Auth:
    base_url: str = BASE_URL

    def __init__(self, api_key: str):
        self._api_key = api_key

    def build_authorization_url(
        self,
        client_id: str,
        integration_id: str,
        redirect_uri: str,
        external_id: Optional[str] = None,
        state: Optional[str] = None,
    ) -> str:
        """Build the hosted authorization URL to send the end user to."""
        return build_authorization_url(
            client_id, integration_id, redirect_uri, external_id, state
        )

    def get_connection_from_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange the one-time code from the redirect for the connection.

        Call this server-side; the code expires after 5 minutes and works once.
        Returns ``{"connection_id", "external_id", "integration_id"}``.
        """
        if not code:
            raise ValueError("code is required")

        if not redirect_uri:
            raise ValueError("redirect_uri is required")

        response = self._connection.post(
            f"{self.base_url}/connection",
            json={"code": code, "redirect_uri": redirect_uri},
        )

        if not response.ok:
            raise Exception(
                f"Failed to get connection: {response.status_code} - {response.text}"
            )

        return dict(response.json())

    @property
    def _connection(self) -> requests.Session:
        request = requests.Session()
        request.headers.update({
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        })
        return request
