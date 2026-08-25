"""
Tests for the shared resource base.

The concrete resources are covered by their own modules; this covers the
behaviour they all inherit.
"""

import pytest
import responses

from bundleup.resources.base import Base

BASE = "https://api.bundleup.io/v1/things"


class Things(Base):
    """Exposes the protected surface so the shared behaviour can be tested once."""

    @property
    def _resource_name(self) -> str:
        return "things"

    def list(self, params=None):
        return self._list(params)

    def create(self, body):
        return self._create(body)

    def retrieve(self, id):
        return self._retrieve(id)

    def update(self, id, body):
        return self._update(id, body)

    def delete(self, id):
        return self._delete(id)

    def url(self, path):
        return self._build_url(path)


@pytest.fixture
def things(api_key):
    return Things(api_key)


class TestUrlBuilding:
    """Where requests are sent."""

    def test_targets_the_versioned_namespace(self, things):
        assert things.url("") == f"{BASE}/"

    def test_appends_the_id_as_a_path_segment(self, things):
        assert things.url("thing_1") == f"{BASE}/thing_1"


class TestHeaders:
    """What every request carries."""

    def test_sends_the_api_key(self, api_key, things, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/", json={})

        things.list()

        headers = mock_responses.calls[0].request.headers
        assert headers["Authorization"] == f"Bearer {api_key}"
        assert headers["Content-Type"] == "application/json"


class TestList:
    """GET the collection."""

    def test_returns_the_payload(self, things, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/", json={"data": [{"id": "1"}]})

        assert things.list() == {"data": [{"id": "1"}]}

    def test_passes_query_params(self, things, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/", json={})

        things.list({"limit": 10, "offset": 20})

        url = mock_responses.calls[0].request.url
        assert "limit=10" in url
        assert "offset=20" in url

    def test_raises_on_failure(self, things, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/", json={}, status=502)

        with pytest.raises(Exception, match="Failed to fetch things: 502"):
            things.list()


class TestCreate:
    """POST to the collection."""

    def test_sends_the_body(self, things, mock_responses):
        mock_responses.add(responses.POST, f"{BASE}/", json={"id": "1"})

        assert things.create({"name": "first"}) == {"id": "1"}

        request = mock_responses.calls[0].request
        assert request.method == "POST"
        assert b"first" in request.body

    def test_raises_on_failure(self, things, mock_responses):
        mock_responses.add(responses.POST, f"{BASE}/", json={}, status=422)

        with pytest.raises(Exception, match="Failed to create things: 422"):
            things.create({})


class TestRetrieve:
    """GET one."""

    def test_fetches_by_id(self, things, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/thing_1", json={"id": "thing_1"})

        assert things.retrieve("thing_1") == {"id": "thing_1"}

    def test_requires_an_id(self, things):
        with pytest.raises(ValueError, match="ID is required for retrieval."):
            things.retrieve(None)

    def test_raises_on_failure(self, things, mock_responses):
        mock_responses.add(responses.GET, f"{BASE}/thing_1", json={}, status=404)

        with pytest.raises(Exception, match="Failed to retrieve things: 404"):
            things.retrieve("thing_1")


class TestUpdate:
    """PUT one."""

    def test_sends_the_body_by_id(self, things, mock_responses):
        mock_responses.add(responses.PUT, f"{BASE}/thing_1", json={"id": "thing_1"})

        things.update("thing_1", {"name": "renamed"})

        request = mock_responses.calls[0].request
        assert request.method == "PUT"
        assert b"renamed" in request.body

    def test_requires_an_id(self, things):
        with pytest.raises(ValueError, match="ID is required for update."):
            things.update(None, {"name": "x"})

    def test_raises_on_failure(self, things, mock_responses):
        mock_responses.add(responses.PUT, f"{BASE}/thing_1", json={}, status=409)

        with pytest.raises(Exception, match="Failed to update things: 409"):
            things.update("thing_1", {})


class TestDelete:
    """DELETE one."""

    def test_deletes_by_id(self, things, mock_responses):
        mock_responses.add(responses.DELETE, f"{BASE}/thing_1", body="", status=204)

        assert things.delete("thing_1") is None
        assert mock_responses.calls[0].request.method == "DELETE"

    def test_requires_an_id(self, things):
        with pytest.raises(ValueError, match="ID is required for deletion."):
            things.delete(None)

    def test_raises_on_failure(self, things, mock_responses):
        mock_responses.add(responses.DELETE, f"{BASE}/thing_1", body="", status=403)

        with pytest.raises(Exception, match="Failed to delete things: 403"):
            things.delete("thing_1")
