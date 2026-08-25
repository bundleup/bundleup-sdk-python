from typing import Any, Dict, Optional, cast
from urllib.parse import quote

from .base import Base
from .types import (
    BranchesResponse,
    CommitsResponse,
    PullsResponse,
    ReleasesResponse,
    ReposResponse,
    TagsResponse,
)


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
        if not repo_name:
            raise ValueError("repo_name is required to fetch pulls.")

        url = self._build_url(f"git/repos/{quote(repo_name, safe='')}/pulls")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name, safe='')}/pulls"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(PullsResponse, response.json())

    def tags(self, repo_name: str, params: Optional[Dict[str, Any]] = None) -> TagsResponse:
        """
        List tags for a specific repository
        """
        if not repo_name:
            raise ValueError("repo_name is required to fetch tags.")

        url = self._build_url(f"git/repos/{quote(repo_name, safe='')}/tags")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name, safe='')}/tags"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(TagsResponse, response.json())

    def releases(self, repo_name: str, params: Optional[Dict[str, Any]] = None) -> ReleasesResponse:
        """
        List releases for a specific repository
        """
        if not repo_name:
            raise ValueError("repo_name is required to fetch releases.")

        url = self._build_url(f"git/repos/{quote(repo_name, safe='')}/releases")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name, safe='')}/releases"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(ReleasesResponse, response.json())

    def branches(self, repo_name: str, params: Optional[Dict[str, Any]] = None) -> BranchesResponse:
        """
        List branches for a specific repository
        """
        if not repo_name:
            raise ValueError("repo_name is required to fetch branches.")

        url = self._build_url(f"git/repos/{quote(repo_name, safe='')}/branches")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name, safe='')}/branches"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(BranchesResponse, response.json())

    def commits(self, repo_name: str, params: Optional[Dict[str, Any]] = None) -> CommitsResponse:
        """
        List commits for a specific repository
        """
        if not repo_name:
            raise ValueError("repo_name is required to fetch commits.")

        url = self._build_url(f"git/repos/{quote(repo_name, safe='')}/commits")
        response = self._connection.get(url, params=params)

        if not response.ok:
            endpoint = f"git/repos/{quote(repo_name, safe='')}/commits"
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(CommitsResponse, response.json())
