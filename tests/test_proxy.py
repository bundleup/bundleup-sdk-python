"""Tests for the Proxy class."""

import pytest
import responses
from bundleup.proxy import Proxy
from bundleup.exceptions import ValidationError, APIError


def test_proxy_init_with_valid_parameters():
    """Test Proxy initialization with valid parameters."""
    proxy = Proxy("test-api-key", "connection-id")
    assert proxy._api_key == "test-api-key"
    assert proxy._connection_id == "connection-id"


def test_proxy_init_with_empty_api_key():
    """Test Proxy initialization with empty API key raises ValidationError."""
    with pytest.raises(ValidationError, match="api_key cannot be empty"):
        Proxy("", "connection-id")


def test_proxy_init_with_empty_connection_id():
    """Test Proxy initialization with empty connection_id raises ValidationError."""
    with pytest.raises(ValidationError, match="connection_id cannot be empty"):
        Proxy("test-api-key", "")


def test_proxy_get_headers():
    """Test _get_headers method."""
    proxy = Proxy("test-api-key", "connection-id")
    headers = proxy._get_headers()
    assert headers["Authorization"] == "Bearer test-api-key"
    assert headers["BU-Connection-Id"] == "connection-id"
    assert headers["Content-Type"] == "application/json"


def test_proxy_get_headers_with_additional_headers():
    """Test _get_headers with additional headers."""
    proxy = Proxy("test-api-key", "connection-id")
    headers = proxy._get_headers({"X-Custom": "value"})
    assert headers["X-Custom"] == "value"


def test_proxy_build_url():
    """Test _build_url method."""
    proxy = Proxy("test-api-key", "connection-id")
    url = proxy._build_url("/users")
    assert url == "https://proxy.bundleup.io/users"


def test_proxy_build_url_without_leading_slash():
    """Test _build_url adds leading slash if missing."""
    proxy = Proxy("test-api-key", "connection-id")
    url = proxy._build_url("users")
    assert url == "https://proxy.bundleup.io/users"


@responses.activate
def test_proxy_get():
    """Test GET method."""
    responses.add(
        responses.GET,
        "https://proxy.bundleup.io/users",
        json={"users": []},
        status=200
    )
    
    proxy = Proxy("test-api-key", "connection-id")
    result = proxy.get("/users")
    assert "users" in result


def test_proxy_get_with_empty_path():
    """Test GET with empty path raises ValidationError."""
    proxy = Proxy("test-api-key", "connection-id")
    with pytest.raises(ValidationError, match="path cannot be empty"):
        proxy.get("")


@responses.activate
def test_proxy_post():
    """Test POST method."""
    responses.add(
        responses.POST,
        "https://proxy.bundleup.io/users",
        json={"id": "123"},
        status=201
    )
    
    proxy = Proxy("test-api-key", "connection-id")
    result = proxy.post("/users", {"name": "John"})
    assert result["id"] == "123"


@responses.activate
def test_proxy_put():
    """Test PUT method."""
    responses.add(
        responses.PUT,
        "https://proxy.bundleup.io/users/123",
        json={"id": "123", "name": "Jane"},
        status=200
    )
    
    proxy = Proxy("test-api-key", "connection-id")
    result = proxy.put("/users/123", {"name": "Jane"})
    assert result["name"] == "Jane"


@responses.activate
def test_proxy_patch():
    """Test PATCH method."""
    responses.add(
        responses.PATCH,
        "https://proxy.bundleup.io/users/123",
        json={"id": "123", "email": "jane@example.com"},
        status=200
    )
    
    proxy = Proxy("test-api-key", "connection-id")
    result = proxy.patch("/users/123", {"email": "jane@example.com"})
    assert result["email"] == "jane@example.com"


@responses.activate
def test_proxy_delete():
    """Test DELETE method."""
    responses.add(
        responses.DELETE,
        "https://proxy.bundleup.io/users/123",
        status=204
    )
    
    proxy = Proxy("test-api-key", "connection-id")
    result = proxy.delete("/users/123")
    assert result is None


@responses.activate
def test_proxy_delete_with_json_response():
    """Test DELETE method with JSON response."""
    responses.add(
        responses.DELETE,
        "https://proxy.bundleup.io/users/123",
        json={"success": True},
        status=200
    )
    
    proxy = Proxy("test-api-key", "connection-id")
    result = proxy.delete("/users/123")
    assert result["success"] is True


def test_proxy_repr():
    """Test __repr__ method."""
    proxy = Proxy("test-api-key", "connection-id")
    assert "Proxy" in repr(proxy)
    assert "connection-id" in repr(proxy)
