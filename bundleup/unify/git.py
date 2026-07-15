from typing import Any, Dict, Optional, cast
from urllib.parse import quote

from .base import Base
from .types import BranchesResponse, PullsResponse, ReleasesResponse, ReposResponse, TagsResponse


class Git(Base):
    def repos(self, params: Optional[Dict[str, Any]] = None) -> ReposResponse:
        """
        List git repositories
        """
        url = self._build_url("git/repos")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch git/repos: {response.status_code}")

        return cast(ReposResponse, response.json())

    def pulls(self, repo_name: str, params: Optional[Dict[str, Any]] = None) -> PullsResponse:
        """
        List pull requests for a specific repository
        """
        url = self._build_url(f"git/repos/{quote(repo_name)}/pulls")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name)}/pulls"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(PullsResponse, response.json())

    def tags(self, repo_name: str, params: Optional[Dict[str, Any]] = None) -> TagsResponse:
        """
        List tags for a specific repository
        """
        url = self._build_url(f"git/repos/{quote(repo_name)}/tags")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name)}/tags"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(TagsResponse, response.json())

    def releases(self, repo_name: str, params: Optional[Dict[str, Any]] = None) -> ReleasesResponse:
        """
        List releases for a specific repository
        """
        url = self._build_url(f"git/repos/{quote(repo_name)}/releases")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name)}/releases"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(ReleasesResponse, response.json())

    def branches(self, repo_name: str, params: Optional[Dict[str, Any]] = None) -> BranchesResponse:
        """
        List branches for a specific repository
        """
        url = self._build_url(f"git/repos/{quote(repo_name)}/branches")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name)}/branches"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(BranchesResponse, response.json())
