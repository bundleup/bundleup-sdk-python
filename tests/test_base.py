"""Tests for the Base class."""

import pytest
import responses
from bundleup.base import Base
from bundleup.exceptions import ValidationError, APIError, AuthenticationError, NotFoundError


class TestResource(Base):
    """Test resource implementation of Base."""
    
    @property
    def _namespace(self):
        return "test-resources"


def test_base_init_with_valid_api_key():
    """Test Base initialization with valid API key."""
    resource = TestResource("test-api-key")
    assert resource._api_key == "test-api-key"


def test_base_init_with_empty_api_key():
    """Test Base initialization with empty API key raises ValidationError."""
    with pytest.raises(ValidationError, match="api_key cannot be empty"):
        TestResource("")


def test_base_headers():
    """Test _headers property returns correct headers."""
    resource = TestResource("test-api-key")
    headers = resource._headers
    assert headers["Authorization"] == "Bearer test-api-key"
    assert headers["Content-Type"] == "application/json"


def test_base_build_url_without_path():
    """Test _build_url without path."""
    resource = TestResource("test-api-key")
    url = resource._build_url()
    assert url == "https://api.bundleup.io/v1/test-resources"


def test_base_build_url_with_path():
    """Test _build_url with path."""
    resource = TestResource("test-api-key")
    url = resource._build_url("123")
    assert url == "https://api.bundleup.io/v1/test-resources/123"


@responses.activate
def test_base_list():
    """Test list method."""
    responses.add(
        responses.GET,
        "https://api.bundleup.io/v1/test-resources",
        json=[{"id": "1"}, {"id": "2"}],
        status=200
    )
    
    resource = TestResource("test-api-key")
    result = resource.list()
    assert len(result) == 2
    assert result[0]["id"] == "1"


@responses.activate
def test_base_create():
    """Test create method."""
    responses.add(
        responses.POST,
        "https://api.bundleup.io/v1/test-resources",
        json={"id": "1", "name": "test"},
        status=201
    )
    
    resource = TestResource("test-api-key")
    result = resource.create({"name": "test"})
    assert result["id"] == "1"
    assert result["name"] == "test"


def test_base_create_with_invalid_data():
    """Test create method with invalid data."""
    resource = TestResource("test-api-key")
    with pytest.raises(ValidationError, match="data must be a dictionary"):
        resource.create("not-a-dict")


@responses.activate
def test_base_retrieve():
    """Test retrieve method."""
    responses.add(
        responses.GET,
        "https://api.bundleup.io/v1/test-resources/123",
        json={"id": "123", "name": "test"},
        status=200
    )
    
    resource = TestResource("test-api-key")
    result = resource.retrieve("123")
    assert result["id"] == "123"


def test_base_retrieve_with_empty_id():
    """Test retrieve method with empty ID."""
    resource = TestResource("test-api-key")
    with pytest.raises(ValidationError, match="id cannot be empty"):
        resource.retrieve("")


@responses.activate
def test_base_update():
    """Test update method."""
    responses.add(
        responses.PATCH,
        "https://api.bundleup.io/v1/test-resources/123",
        json={"id": "123", "name": "updated"},
        status=200
    )
    
    resource = TestResource("test-api-key")
    result = resource.update("123", {"name": "updated"})
    assert result["name"] == "updated"


def test_base_update_with_empty_id():
    """Test update method with empty ID."""
    resource = TestResource("test-api-key")
    with pytest.raises(ValidationError, match="id cannot be empty"):
        resource.update("", {"name": "test"})


def test_base_update_with_invalid_data():
    """Test update method with invalid data."""
    resource = TestResource("test-api-key")
    with pytest.raises(ValidationError, match="data must be a dictionary"):
        resource.update("123", "not-a-dict")


@responses.activate
def test_base_delete():
    """Test delete method."""
    responses.add(
        responses.DELETE,
        "https://api.bundleup.io/v1/test-resources/123",
        status=204
    )
    
    resource = TestResource("test-api-key")
    resource.delete("123")  # Should not raise


def test_base_delete_with_empty_id():
    """Test delete method with empty ID."""
    resource = TestResource("test-api-key")
    with pytest.raises(ValidationError, match="id cannot be empty"):
        resource.delete("")


@responses.activate
def test_base_authentication_error():
    """Test authentication error handling."""
    responses.add(
        responses.GET,
        "https://api.bundleup.io/v1/test-resources",
        json={"error": "Unauthorized"},
        status=401
    )
    
    resource = TestResource("test-api-key")
    with pytest.raises(AuthenticationError):
        resource.list()


@responses.activate
def test_base_not_found_error():
    """Test not found error handling."""
    responses.add(
        responses.GET,
        "https://api.bundleup.io/v1/test-resources/999",
        json={"error": "Not found"},
        status=404
    )
    
    resource = TestResource("test-api-key")
    with pytest.raises(NotFoundError):
        resource.retrieve("999")


def test_base_repr():
    """Test __repr__ method."""
    resource = TestResource("test-api-key")
    assert "TestResource" in repr(resource)
    assert "test-resources" in repr(resource)
