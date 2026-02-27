from .base import Base


class PM(Base):
    def issues(self, params: dict = None):
        """
        List project-management issues
        """
        url = self._build_url("pm/issues")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch pm/issues: {response.status_code}")

        return response.json()
