from typing import Any, Dict, Optional, cast

from .base import Base
from .types import FilesResponse


class Drive(Base):
    def files(self, params: Optional[Dict[str, Any]] = None) -> FilesResponse:
        """
        List Drive files
        """
        url = self._build_url("drive/files")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch drive/files: {response.status_code}")

        return cast(FilesResponse, response.json())
