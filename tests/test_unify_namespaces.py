"""
Tests for the Unify namespaces' HTTP behaviour.

test_unify.py covers construction and wiring; this covers what each namespace
actually sends and how it handles failures.
"""

import pytest
import responses

from bundleup.unify.chat import Chat
from bundleup.unify.crm import CRM
from bundleup.unify.drive import Drive
from bundleup.unify.git import Git
from bundleup.unify.ticketing import Ticketing

BASE = "https://unify.bundleup.io/v1"

PAGE = {"data": [], "metadata": {"next": None}}


class TestBase:
    """Shared URL and header construction."""

    def test_targets_the_versioned_namespace(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/chat/users", json=PAGE)

        Chat(api_key, connection_id).users()

        assert mock_responses.calls[0].request.url.startswith(f"{BASE}/chat/users")

    def test_sends_the_api_key_and_connection_id(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/chat/users", json=PAGE)

        Chat(api_key, connection_id).users()

        headers = mock_responses.calls[0].request.headers
        assert headers["Authorization"] == f"Bearer {api_key}"
        assert headers["BU-Connection-Id"] == connection_id
        assert headers["Content-Type"] == "application/json"

    def test_passes_query_params_through(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/chat/users", json=PAGE)

        Chat(api_key, connection_id).users({"limit": 5, "after": "cursor_1"})

        url = mock_responses.calls[0].request.url
        assert "limit=5" in url
        assert "after=cursor_1" in url

    def test_returns_the_parsed_body(self, api_key, connection_id, mock_responses):
        payload = {"data": [{"id": "u_1", "name": "Ada"}], "metadata": {"next": "cursor_2"}}
        mock_responses.add(responses.GET, f"{BASE}/chat/users", json=payload)

        assert Chat(api_key, connection_id).users() == payload


class TestChat:
    """chat/*"""

    @pytest.mark.parametrize(
        "method,path", [("users", "chat/users"), ("channels", "chat/channels")]
    )
    def test_fetches(self, api_key, connection_id, mock_responses, method, path):
        mock_responses.add(responses.GET, f"{BASE}/{path}", json=PAGE)

        getattr(Chat(api_key, connection_id), method)()

        assert mock_responses.calls[0].request.url.startswith(f"{BASE}/{path}")

    @pytest.mark.parametrize(
        "method,path", [("users", "chat/users"), ("channels", "chat/channels")]
    )
    def test_raises_on_failure(self, api_key, connection_id, mock_responses, method, path):
        mock_responses.add(responses.GET, f"{BASE}/{path}", json={}, status=502)

        with pytest.raises(Exception, match=f"Failed to fetch {path}: 502"):
            getattr(Chat(api_key, connection_id), method)()

    def test_posts_a_message(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.POST, f"{BASE}/chat/channels/C123/message", json={"data": {}})

        Chat(api_key, connection_id).message("C123", "Deploy finished")

        request = mock_responses.calls[0].request
        assert request.method == "POST"
        assert b"Deploy finished" in request.body

    def test_encodes_the_channel_id(self, api_key, connection_id, mock_responses):
        url = f"{BASE}/chat/channels/team%2Fgeneral/message"
        mock_responses.add(responses.POST, url, json={"data": {}})

        Chat(api_key, connection_id).message("team/general", "hi")

        assert "team%2Fgeneral" in mock_responses.calls[0].request.url

    def test_requires_a_channel_id(self, api_key, connection_id):
        with pytest.raises(ValueError, match="channel_id is required to send a message."):
            Chat(api_key, connection_id).message("", "hi")

    def test_raises_when_the_message_fails(self, api_key, connection_id, mock_responses):
        url = f"{BASE}/chat/channels/C123/message"
        mock_responses.add(responses.POST, url, json={}, status=403)

        with pytest.raises(Exception, match="Failed to post chat/channels/C123/message: 403"):
            Chat(api_key, connection_id).message("C123", "hi")


class TestCRM:
    """crm/*"""

    @pytest.mark.parametrize(
        "method,path", [("companies", "crm/companies"), ("contacts", "crm/contacts")]
    )
    def test_fetches(self, api_key, connection_id, mock_responses, method, path):
        mock_responses.add(responses.GET, f"{BASE}/{path}", json=PAGE)

        getattr(CRM(api_key, connection_id), method)()

        assert mock_responses.calls[0].request.url.startswith(f"{BASE}/{path}")

    @pytest.mark.parametrize(
        "method,path", [("companies", "crm/companies"), ("contacts", "crm/contacts")]
    )
    def test_raises_on_failure(self, api_key, connection_id, mock_responses, method, path):
        mock_responses.add(responses.GET, f"{BASE}/{path}", json={}, status=502)

        with pytest.raises(Exception, match=f"Failed to fetch {path}: 502"):
            getattr(CRM(api_key, connection_id), method)()


class TestDrive:
    """drive/*"""

    def test_fetches_files(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/drive/files", json=PAGE)

        Drive(api_key, connection_id).files()

        assert mock_responses.calls[0].request.url.startswith(f"{BASE}/drive/files")

    def test_raises_on_failure(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/drive/files", json={}, status=502)

        with pytest.raises(Exception, match="Failed to fetch drive/files: 502"):
            Drive(api_key, connection_id).files()


class TestTicketing:
    """ticketing/*"""

    def test_fetches_tickets(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/ticketing/tickets", json=PAGE)

        Ticketing(api_key, connection_id).tickets()

        assert mock_responses.calls[0].request.url.startswith(f"{BASE}/ticketing/tickets")

    def test_raises_on_failure(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/ticketing/tickets", json={}, status=502)

        with pytest.raises(Exception, match="Failed to fetch ticketing/tickets: 502"):
            Ticketing(api_key, connection_id).tickets()


SCOPED = ["pulls", "tags", "releases", "branches", "commits"]


class TestGit:
    """git/*"""

    def test_fetches_repos(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/git/repos", json=PAGE)

        Git(api_key, connection_id).repos()

        assert mock_responses.calls[0].request.url.startswith(f"{BASE}/git/repos")

    def test_raises_when_repos_fails(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/git/repos", json={}, status=502)

        with pytest.raises(Exception, match="Failed to fetch git/repos: 502"):
            Git(api_key, connection_id).repos()

    @pytest.mark.parametrize("method", SCOPED)
    def test_fetches_for_a_repo(self, api_key, connection_id, mock_responses, method):
        path = f"git/repos/acme%2Fapi/{method}"
        mock_responses.add(responses.GET, f"{BASE}/{path}", json=PAGE)

        getattr(Git(api_key, connection_id), method)("acme/api")

        assert "acme%2Fapi" in mock_responses.calls[0].request.url

    @pytest.mark.parametrize("method", SCOPED)
    def test_requires_a_repo_name(self, api_key, connection_id, method):
        with pytest.raises(ValueError, match=f"repo_name is required to fetch {method}."):
            getattr(Git(api_key, connection_id), method)("")

    @pytest.mark.parametrize("method", SCOPED)
    def test_raises_on_failure(self, api_key, connection_id, mock_responses, method):
        path = f"git/repos/acme%2Fapi/{method}"
        mock_responses.add(responses.GET, f"{BASE}/{path}", json={}, status=404)

        with pytest.raises(Exception, match=f"Failed to fetch git/repos/acme%2Fapi/{method}: 404"):
            getattr(Git(api_key, connection_id), method)("acme/api")

    @pytest.mark.parametrize("method", SCOPED)
    def test_passes_params_through(self, api_key, connection_id, mock_responses, method):
        path = f"git/repos/acme%2Fapi/{method}"
        mock_responses.add(responses.GET, f"{BASE}/{path}", json=PAGE)

        getattr(Git(api_key, connection_id), method)("acme/api", {"limit": 5})

        assert "limit=5" in mock_responses.calls[0].request.url
