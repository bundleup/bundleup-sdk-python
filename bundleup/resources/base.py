from abc import ABC, abstractmethod
from urllib.parse import urljoin

import requests


class Base(ABC):
    base_url = "https://api.bundleup.io"
    version = "v1"

    def __init__(self, api_key: str):
        self._api_key = api_key

    @property
    @abstractmethod
    def _resource_name(self):
        pass

    def _list(self, params: dict = None):
        url = self._build_url("")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch {self._resource_name}: {response.status_code}")

        return response.json()

    def _create(self, body: dict):
        url = self._build_url("")
        response = self._connection.post(url, json=body)

        if not response.ok:
            raise Exception(f"Failed to create {self._resource_name}: {response.status_code}")

        return response.json()

    def _retrieve(self, id: str):
        if id is None:
            raise ValueError("ID is required for retrieval.")

        url = self._build_url(id)
        response = self._connection.get(url)

        if not response.ok:
            raise Exception(f"Failed to retrieve {self._resource_name}: {response.status_code}")

        return response.json()

    def _update(self, id: str, body: dict):
        if id is None:
            raise ValueError("ID is required for update.")

        url = self._build_url(id)
        response = self._connection.put(url, json=body)

        if not response.ok:
            raise Exception(f"Failed to update {self._resource_name}: {response.status_code}")

        return response.json()

    def _delete(self, id: str):
        if id is None:
            raise ValueError("ID is required for deletion.")

        url = self._build_url(id)
        response = self._connection.delete(url)

        if not response.ok:
            raise Exception(f"Failed to delete {self._resource_name}: {response.status_code}")

        return None

    @property
    def _connection(self):
        request = requests.Session()
        request.headers.update({
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        })
        return request

    def _build_url(self, path: str):
        return urljoin(f"{self.base_url}/{self.version}/{self._resource_name}/", path)
