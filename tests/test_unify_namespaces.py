"""
Tests for the Unify namespaces' HTTP behaviour.

test_unify.py covers construction and wiring; this covers what each namespace
actually sends and how it handles failures.
"""

import pytest
import responses

from bundleup.unify.chat import Chat
from bundleup.unify.crm import CRM
from bundleup.unify.calendar import Calendar
from bundleup.unify.drive import Drive
from bundleup.unify.git import Git
from bundleup.unify.me import Me
from bundleup.unify.ticketing import Ticketing
from bundleup.unify import Unify

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

    def test_fetches_messages(self, api_key, connection_id, mock_responses):
        url = f"{BASE}/chat/channels/C123/messages"
        mock_responses.add(responses.GET, url, json=PAGE)

        Chat(api_key, connection_id).messages("C123")

        assert mock_responses.calls[0].request.url.startswith(url)

    def test_encodes_the_channel_id_for_messages(self, api_key, connection_id, mock_responses):
        url = f"{BASE}/chat/channels/team%2Fgeneral/messages"
        mock_responses.add(responses.GET, url, json=PAGE)

        Chat(api_key, connection_id).messages("team/general")

        assert "team%2Fgeneral/messages" in mock_responses.calls[0].request.url

    def test_requires_a_channel_id_for_messages(self, api_key, connection_id):
        with pytest.raises(ValueError, match="channel_id is required to fetch messages."):
            Chat(api_key, connection_id).messages("")

    def test_raises_when_messages_fail(self, api_key, connection_id, mock_responses):
        url = f"{BASE}/chat/channels/C123/messages"
        mock_responses.add(responses.GET, url, json={}, status=404)

        with pytest.raises(Exception, match="Failed to fetch chat/channels/C123/messages: 404"):
            Chat(api_key, connection_id).messages("C123")


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


class TestCalendar:
    """calendar/*"""

    WINDOW = {"starts_after": "2026-09-01T00:00:00Z", "starts_before": "2026-09-08T00:00:00Z"}

    def test_fetches_events(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/calendar/events", json=PAGE)

        Calendar(api_key, connection_id).events(self.WINDOW)

        assert mock_responses.calls[0].request.url.startswith(f"{BASE}/calendar/events")

    def test_passes_through_the_window(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/calendar/events", json=PAGE)

        Calendar(api_key, connection_id).events(self.WINDOW)

        url = mock_responses.calls[0].request.url

        assert "starts_after=2026-09-01T00%3A00%3A00Z" in url
        assert "starts_before=2026-09-08T00%3A00%3A00Z" in url

    @pytest.mark.parametrize(
        "params",
        [
            None,
            {},
            {"starts_after": "2026-09-01T00:00:00Z"},
            {"starts_before": "2026-09-08T00:00:00Z"},
        ],
    )
    def test_requires_the_window(self, api_key, connection_id, params):
        with pytest.raises(ValueError, match="starts_after and starts_before are required"):
            Calendar(api_key, connection_id).events(params)

    def test_raises_on_failure(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/calendar/events", json={}, status=502)

        with pytest.raises(Exception, match="Failed to fetch calendar/events: 502"):
            Calendar(api_key, connection_id).events(self.WINDOW)


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

    def test_fetches_a_single_ticket(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/ticketing/tickets/TKT-1", json={"data": {}})

        Ticketing(api_key, connection_id).ticket("TKT-1")

        assert mock_responses.calls[0].request.url.startswith(f"{BASE}/ticketing/tickets/TKT-1")

    def test_encodes_the_ticket_id(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/ticketing/tickets/a%2Fb", json={"data": {}})

        Ticketing(api_key, connection_id).ticket("a/b")

        assert "ticketing/tickets/a%2Fb" in mock_responses.calls[0].request.url

    def test_requires_a_ticket_id(self, api_key, connection_id):
        with pytest.raises(ValueError, match="ticket_id is required"):
            Ticketing(api_key, connection_id).ticket("")

    def test_raises_when_a_single_ticket_fails(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/ticketing/tickets/TKT-1", json={}, status=404)

        with pytest.raises(Exception, match="Failed to fetch ticketing/tickets/TKT-1: 404"):
            Ticketing(api_key, connection_id).ticket("TKT-1")


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


ACCOUNT = {"data": {"id": "u_1", "name": "Ada", "email": "ada@acme.io", "avatar_url": None}}


class TestMe:
    """me"""

    def test_targets_the_root_endpoint_not_a_vertical(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/me", json=ACCOUNT)

        Me(api_key, connection_id).get()

        assert mock_responses.calls[0].request.url.rstrip("/") == f"{BASE}/me"

    def test_sends_the_api_key_and_connection_id(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/me", json=ACCOUNT)

        Me(api_key, connection_id).get()

        headers = mock_responses.calls[0].request.headers
        assert headers["Authorization"] == f"Bearer {api_key}"
        assert headers["BU-Connection-Id"] == connection_id

    def test_passes_include_raw_through(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/me", json=ACCOUNT)

        Me(api_key, connection_id).get({"include_raw": "true"})

        assert "include_raw=true" in mock_responses.calls[0].request.url

    def test_returns_the_parsed_account(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/me", json=ACCOUNT)

        assert Me(api_key, connection_id).get() == ACCOUNT

    def test_raises_on_failure(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/me", json={}, status=502)

        with pytest.raises(Exception, match="Failed to fetch me: 502"):
            Me(api_key, connection_id).get()

    def test_is_reachable_from_the_unify_client(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/me", json=ACCOUNT)

        assert Unify(api_key, connection_id).me() == ACCOUNT
