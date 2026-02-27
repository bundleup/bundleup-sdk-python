from urllib.parse import quote

from .base import Base


class Git(Base):
    def repos(self, params: dict = None):
        """
        List git repositories
        """
        url = self._build_url("git/repos")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch git/repos: {response.status_code}")

        return response.json()

    def pulls(self, repo_name: str, params: dict = None):
        """
        List pull requests for a specific repository
        """
        url = self._build_url(f"git/repos/{quote(repo_name)}/pulls")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name)}/pulls"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return response.json()

    def tags(self, repo_name: str, params: dict = None):
        """
        List tags for a specific repository
        """
        url = self._build_url(f"git/repos/{quote(repo_name)}/tags")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name)}/tags"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return response.json()

    def releases(self, repo_name: str, params: dict = None):
        """
        List releases for a specific repository
        """
        url = self._build_url(f"git/repos/{quote(repo_name)}/releases")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name)}/releases"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return response.json()
