"""
Tests for the Proxy class.
"""

import responses
from bundleup.proxy import Proxy


class TestProxyInitialization:
    """Test Proxy class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        proxy = Proxy(api_key, connection_id)

        assert proxy._api_key == api_key
        assert proxy._connection_id == connection_id
        assert proxy.base_url == "https://proxy.bundleup.io"

    def test_connection_headers(self, api_key, connection_id):
        """Test that connection headers are properly set."""
        proxy = Proxy(api_key, connection_id)
        conn = proxy._connection

        assert conn.headers["Authorization"] == f"Bearer {api_key}"
        assert conn.headers["BU-Connection-Id"] == connection_id
        assert conn.headers["Content-Type"] == "application/json"


class TestProxyURLBuilding:
    """Test URL building in Proxy."""

    def test_build_url_with_absolute_path(self, api_key, connection_id):
        """Test building URL with absolute path."""
        proxy = Proxy(api_key, connection_id)
        url = proxy._build_url("/users")

        assert url == "https://proxy.bundleup.io/users"

    def test_build_url_with_relative_path(self, api_key, connection_id):
        """Test building URL with relative path."""
        proxy = Proxy(api_key, connection_id)
        url = proxy._build_url("users")

        assert url == "https://proxy.bundleup.io/users"

    def test_build_url_with_nested_path(self, api_key, connection_id):
        """Test building URL with nested path."""
        proxy = Proxy(api_key, connection_id)
        url = proxy._build_url("/api/v1/users/123")

        assert url == "https://proxy.bundleup.io/api/v1/users/123"


class TestProxyGetMethod:
    """Test Proxy GET method."""

    @responses.activate
    def test_get_request(self, api_key, connection_id):
        """Test making a GET request."""
        responses.add(
            responses.GET,
            "https://proxy.bundleup.io/users",
            json={"data": [{"id": "1", "name": "John"}]},
            status=200
        )

        proxy = Proxy(api_key, connection_id)
        response = proxy.get("/users")

        assert response.status_code == 200
        assert response.json()["data"][0]["name"] == "John"

    @responses.activate
    def test_get_request_with_params(self, api_key, connection_id):
        """Test making a GET request with query parameters."""
        responses.add(
            responses.GET,
            "https://proxy.bundleup.io/users?limit=10&offset=0",
            json={"data": []},
            status=200
        )

        proxy = Proxy(api_key, connection_id)
        response = proxy.get("/users", params={"limit": 10, "offset": 0})

        assert response.status_code == 200

    @responses.activate
    def test_get_request_with_custom_headers(self, api_key, connection_id):
        """Test making a GET request with custom headers."""
        def request_callback(request):
            assert request.headers.get("X-Custom-Header") == "custom-value"
            return (200, {}, '{"data": []}')

        responses.add_callback(
            responses.GET,
            "https://proxy.bundleup.io/users",
            callback=request_callback
        )

        proxy = Proxy(api_key, connection_id)
        _ = proxy.get("/users", headers={"X-Custom-Header": "custom-value"})


class TestProxyPostMethod:
    """Test Proxy POST method."""

    @responses.activate
    def test_post_request(self, api_key, connection_id):
        """Test making a POST request."""
        responses.add(
            responses.POST,
            "https://proxy.bundleup.io/users",
            json={"id": "123", "name": "John"},
            status=201
        )

        proxy = Proxy(api_key, connection_id)
        response = proxy.post("/users", body={"name": "John"})

        assert response.status_code == 201
        assert response.json()["id"] == "123"

    @responses.activate
    def test_post_request_with_custom_headers(self, api_key, connection_id):
        """Test making a POST request with custom headers."""
        def request_callback(request):
            assert request.headers.get("X-Custom-Header") == "custom-value"
            return (201, {}, '{"id": "123"}')

        responses.add_callback(
            responses.POST,
            "https://proxy.bundleup.io/users",
            callback=request_callback
        )

        proxy = Proxy(api_key, connection_id)
        _ = proxy.post(
            "/users",
            body={"name": "John"},
            headers={"X-Custom-Header": "custom-value"},
        )


class TestProxyPutMethod:
    """Test Proxy PUT method."""

    @responses.activate
    def test_put_request(self, api_key, connection_id):
        """Test making a PUT request."""
        responses.add(
            responses.PUT,
            "https://proxy.bundleup.io/users/123",
            json={"id": "123", "name": "Jane"},
            status=200
        )

        proxy = Proxy(api_key, connection_id)
        response = proxy.put("/users/123", body={"name": "Jane"})

        assert response.status_code == 200
        assert response.json()["name"] == "Jane"


class TestProxyPatchMethod:
    """Test Proxy PATCH method."""

    @responses.activate
    def test_patch_request(self, api_key, connection_id):
        """Test making a PATCH request."""
        responses.add(
            responses.PATCH,
            "https://proxy.bundleup.io/users/123",
            json={"id": "123", "email": "jane@example.com"},
            status=200
        )

        proxy = Proxy(api_key, connection_id)
        response = proxy.patch("/users/123", body={"email": "jane@example.com"})

        assert response.status_code == 200
        assert response.json()["email"] == "jane@example.com"


class TestProxyDeleteMethod:
    """Test Proxy DELETE method."""

    @responses.activate
    def test_delete_request(self, api_key, connection_id):
        """Test making a DELETE request."""
        responses.add(
            responses.DELETE,
            "https://proxy.bundleup.io/users/123",
            status=204
        )

        proxy = Proxy(api_key, connection_id)
        response = proxy.delete("/users/123")

        assert response.status_code == 204

    @responses.activate
    def test_delete_request_with_custom_headers(self, api_key, connection_id):
        """Test making a DELETE request with custom headers."""
        def request_callback(request):
            assert request.headers.get("X-Custom-Header") == "custom-value"
            return (204, {}, '')

        responses.add_callback(
            responses.DELETE,
            "https://proxy.bundleup.io/users/123",
            callback=request_callback
        )

        proxy = Proxy(api_key, connection_id)
        _ = proxy.delete("/users/123", headers={"X-Custom-Header": "custom-value"})
