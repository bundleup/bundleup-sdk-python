"""Tests for the main BundleUp client."""

import pytest
from bundleup import BundleUp
from bundleup.connection import Connections
from bundleup.integration import Integrations
from bundleup.webhooks import Webhooks
from bundleup.proxy import Proxy
from bundleup.unify import Unify


def test_bundleup_init_with_valid_api_key():
    """Test BundleUp initialization with valid API key."""
    client = BundleUp("test-api-key")
    assert client._api_key == "test-api-key"


def test_bundleup_init_with_empty_api_key():
    """Test BundleUp initialization with empty API key raises ValueError."""
    with pytest.raises(ValueError, match="api_key cannot be empty"):
        BundleUp("")


def test_bundleup_init_with_none_api_key():
    """Test BundleUp initialization with None API key raises ValueError."""
    with pytest.raises(ValueError, match="api_key must be a string"):
        BundleUp(None)


def test_bundleup_connections_property():
    """Test connections property returns Connections instance."""
    client = BundleUp("test-api-key")
    assert isinstance(client.connections, Connections)


def test_bundleup_integrations_property():
    """Test integrations property returns Integrations instance."""
    client = BundleUp("test-api-key")
    assert isinstance(client.integrations, Integrations)


def test_bundleup_webhooks_property():
    """Test webhooks property returns Webhooks instance."""
    client = BundleUp("test-api-key")
    assert isinstance(client.webhooks, Webhooks)


def test_bundleup_proxy_method():
    """Test proxy method returns Proxy instance."""
    client = BundleUp("test-api-key")
    proxy = client.proxy("connection-id")
    assert isinstance(proxy, Proxy)
    assert proxy._connection_id == "connection-id"


def test_bundleup_proxy_method_with_empty_connection_id():
    """Test proxy method with empty connection_id raises ValueError."""
    client = BundleUp("test-api-key")
    with pytest.raises(ValueError, match="connection_id cannot be empty"):
        client.proxy("")


def test_bundleup_unify_method():
    """Test unify method returns Unify instance."""
    client = BundleUp("test-api-key")
    unify = client.unify("connection-id")
    assert isinstance(unify, Unify)
    assert unify._connection_id == "connection-id"


def test_bundleup_unify_method_with_empty_connection_id():
    """Test unify method with empty connection_id raises ValueError."""
    client = BundleUp("test-api-key")
    with pytest.raises(ValueError, match="connection_id cannot be empty"):
        client.unify("")
