from typing import Any, Dict, Optional, cast
from urllib.parse import quote

from .base import Base
from .types import ProjectsResponse, TaskResponse, TasksResponse


class Tasks(Base):
    def tasks(self, params: Optional[Dict[str, Any]] = None) -> TasksResponse:
        """
        List tasks from an issue tracker or project tool
        """
        url = self._build_url("tasks/tasks")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch tasks/tasks: {response.status_code}")

        return cast(TasksResponse, response.json())

    def task(self, task_id: str, params: Optional[Dict[str, Any]] = None) -> TaskResponse:
        """
        Get a single task by ID

        Not supported by Basecamp, whose API only serves a to-do underneath its
        project — an id on its own cannot address one.
        """
        if not task_id:
            raise ValueError("task_id is required to fetch a task.")

        endpoint = f"tasks/tasks/{quote(str(task_id), safe='')}"
        url = self._build_url(endpoint)
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch {endpoint}: {response.status_code}")

        return cast(TaskResponse, response.json())

    def projects(self, params: Optional[Dict[str, Any]] = None) -> ProjectsResponse:
        """
        List projects from an issue tracker or project tool
        """
        url = self._build_url("tasks/projects")
        response = self._connection.get(url, params=params)

        if not response.ok:
            raise Exception(f"Failed to fetch tasks/projects: {response.status_code}")

        return cast(ProjectsResponse, response.json())
