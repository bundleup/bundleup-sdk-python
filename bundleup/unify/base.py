from urllib.parse import urljoin

import requests


class Base:
    base_url = "https://unify.bundleup.io"
    version = "v1"

    def __init__(self, api_key: str, connection_id: str):
        self._api_key = api_key
        self._connection_id = connection_id

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
        return urljoin(f"{self.base_url}/{self.version}/", path)
