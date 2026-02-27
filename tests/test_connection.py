"""
Tests for the Connection resource.
"""

import pytest
import responses
from bundleup.resources.connection import Connection


class TestConnectionInitialization:
    """Test Connection resource initialization."""

    def test_init_with_api_key(self, api_key):
        """Test initialization with valid API key."""
        connection = Connection(api_key)

        assert connection._api_key == api_key
        assert connection._resource_name == "connections"

    def test_base_url(self, api_key):
        """Test base URL is correctly set."""
        connection = Connection(api_key)

        assert connection.base_url == "https://api.bundleup.io"
        assert connection.version == "v1"

    def test_connection_headers(self, api_key):
        """Test that connection headers are properly set."""
        connection = Connection(api_key)
        conn = connection._connection

        assert conn.headers["Authorization"] == f"Bearer {api_key}"
        assert conn.headers["Content-Type"] == "application/json"


class TestConnectionList:
    """Test Connection list method."""

    @responses.activate
    def test_list_connections(self, api_key):
        """Test listing all connections."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/connections/",
            json={
                "data": [
                    {"id": "conn_1", "name": "Connection 1"},
                    {"id": "conn_2", "name": "Connection 2"}
                ]
            },
            status=200
        )

        connection = Connection(api_key)
        result = connection.list()

        assert "data" in result
        data = result["data"]
        assert len(data) == 2
        assert data[0]["id"] == "conn_1"

    @responses.activate
    def test_list_connections_with_params(self, api_key):
        """Test listing connections with query parameters."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/connections/?limit=10&status=active",
            json={"data": []},
            status=200
        )

        connection = Connection(api_key)
        result = connection.list(params={"limit": 10, "status": "active"})

        assert "data" in result
        assert result["data"] == []

    @responses.activate
    def test_list_connections_empty(self, api_key):
        """Test listing connections when none exist."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/connections/",
            json={"data": []},
            status=200
        )

        connection = Connection(api_key)
        result = connection.list()

        assert "data" in result
        assert result["data"] == []


class TestConnectionRetrieve:
    """Test Connection retrieve method."""

    @responses.activate
    def test_retrieve_connection(self, api_key, connection_id):
        """Test retrieving a specific connection."""
        responses.add(
            responses.GET,
            f"https://api.bundleup.io/v1/connections/{connection_id}",
            json={"id": connection_id, "name": "Test Connection"},
            status=200
        )

        connection = Connection(api_key)
        result = connection.retrieve(connection_id)

        assert result["id"] == connection_id
        assert result["name"] == "Test Connection"

    def test_retrieve_connection_without_id(self, api_key):
        """Test retrieving a connection without ID raises ValueError."""
        connection = Connection(api_key)

        with pytest.raises(ValueError) as exc_info:
            connection.retrieve(None)

        assert "ID is required for retrieval" in str(exc_info.value)

    @responses.activate
    def test_retrieve_connection_not_found(self, api_key):
        """Test retrieving a non-existent connection."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/connections/nonexistent",
            json={"error": "Connection not found"},
            status=404
        )

        connection = Connection(api_key)
        with pytest.raises(Exception) as exc_info:
            connection.retrieve("nonexistent")

        assert "Failed to retrieve" in str(exc_info.value)
        assert "404" in str(exc_info.value)


class TestConnectionDelete:
    """Test Connection delete method."""

    @responses.activate
    def test_delete_connection(self, api_key, connection_id):
        """Test deleting a connection."""
        responses.add(
            responses.DELETE,
            f"https://api.bundleup.io/v1/connections/{connection_id}",
            status=204
        )

        connection = Connection(api_key)
        result = connection.delete(connection_id)

        # 204 returns None
        assert result is None
        assert len(responses.calls) == 1

    def test_delete_connection_without_id(self, api_key):
        """Test deleting a connection without ID raises ValueError."""
        connection = Connection(api_key)

        with pytest.raises(ValueError) as exc_info:
            connection.delete(None)

        assert "ID is required for deletion" in str(exc_info.value)

    @responses.activate
    def test_delete_connection_not_found(self, api_key):
        """Test deleting a non-existent connection."""
        responses.add(
            responses.DELETE,
            "https://api.bundleup.io/v1/connections/nonexistent",
            json={"error": "Connection not found"},
            status=404
        )

        connection = Connection(api_key)
        with pytest.raises(Exception) as exc_info:
            connection.delete("nonexistent")

        assert "Failed to delete" in str(exc_info.value)
        assert "404" in str(exc_info.value)


class TestConnectionURLBuilding:
    """Test URL building in Connection resource."""

    def test_build_url_for_list(self, api_key):
        """Test building URL for list endpoint."""
        connection = Connection(api_key)
        url = connection._build_url("")

        assert url == "https://api.bundleup.io/v1/connections/"

    def test_build_url_for_specific_resource(self, api_key, connection_id):
        """Test building URL for specific resource."""
        connection = Connection(api_key)
        url = connection._build_url(connection_id)

        assert url == f"https://api.bundleup.io/v1/connections/{connection_id}"
