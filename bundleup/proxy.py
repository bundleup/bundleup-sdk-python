from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests


class Proxy:
    base_url: str = "https://proxy.bundleup.io"

    def __init__(self, api_key: str, connection_id: str):
        self._api_key = api_key
        self._connection_id = connection_id

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = self._build_url(path)
        return self._connection.get(url, params=params, headers=headers)

    def post(
        self,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = self._build_url(path)
        return self._connection.post(url, json=body, headers=headers)

    def put(
        self,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = self._build_url(path)
        return self._connection.put(url, json=body, headers=headers)

    def patch(
        self,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = self._build_url(path)
        return self._connection.patch(url, json=body, headers=headers)

    def delete(self, path: str, headers: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = self._build_url(path)
        return self._connection.delete(url, headers=headers)

    @property
    def _connection(self) -> requests.Session:
        request = requests.Session()
        request.headers.update({
            "Authorization": f"Bearer {self._api_key}",
            "BU-Connection-Id": self._connection_id,
            "Content-Type": "application/json"
        })
        return request

    def _build_url(self, path: str) -> str:
        return urljoin(self.base_url, path)
