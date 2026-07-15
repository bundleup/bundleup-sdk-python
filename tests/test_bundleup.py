"""
Tests for the main BundleUp class.
"""

import pytest
from bundleup import BundleUp
from bundleup.proxy import Proxy
from bundleup.unify import Unify
from bundleup.resources.connection import Connection
from bundleup.resources.integration import Integration
from bundleup.resources.webhook import Webhook


class TestBundleUpInitialization:
    """Test BundleUp class initialization."""

    def test_init_with_api_key(self, api_key):
        """Test initialization with valid API key."""
        client = BundleUp(api_key)

        assert client._api_key == api_key
        assert isinstance(client.connection, Connection)
        assert isinstance(client.integration, Integration)
        assert isinstance(client.webhook, Webhook)

    def test_init_without_api_key(self):
        """Test initialization without API key raises exception."""
        with pytest.raises(Exception) as exc_info:
            BundleUp(None)

        assert "API key is required" in str(exc_info.value)

    def test_init_with_empty_api_key(self):
        """Test initialization with empty API key."""
        # Note: Empty string is not None, so it should work
        client = BundleUp("")
        assert client._api_key == ""


class TestBundleUpProxy:
    """Test BundleUp proxy method."""

    def test_proxy_with_connection_id(self, api_key, connection_id):
        """Test creating a proxy with valid connection ID."""
        client = BundleUp(api_key)
        proxy = client.proxy(connection_id)

        assert isinstance(proxy, Proxy)
        assert proxy._api_key == api_key
        assert proxy._connection_id == connection_id

    def test_proxy_without_connection_id(self, api_key):
        """Test creating a proxy without connection ID raises exception."""
        client = BundleUp(api_key)

        with pytest.raises(Exception) as exc_info:
            client.proxy(None)

        assert "Connection ID is required" in str(exc_info.value)


class TestBundleUpUnify:
    """Test BundleUp unify method."""

    def test_unify_with_connection_id(self, api_key, connection_id):
        """Test creating a unify client with valid connection ID."""
        client = BundleUp(api_key)
        unify = client.unify(connection_id)

        assert isinstance(unify, Unify)
        assert unify.chat._api_key == api_key
        assert unify.chat._connection_id == connection_id
        assert unify.git._api_key == api_key
        assert unify.git._connection_id == connection_id
        assert unify.ticketing._api_key == api_key
        assert unify.ticketing._connection_id == connection_id

    def test_unify_without_connection_id(self, api_key):
        """Test creating a unify client without connection ID raises exception."""
        client = BundleUp(api_key)

        with pytest.raises(Exception) as exc_info:
            client.unify(None)

        assert "Connection ID is required" in str(exc_info.value)


class TestBundleUpResources:
    """Test BundleUp resource access."""

    def test_connection_resource(self, api_key):
        """Test connection resource is properly initialized."""
        client = BundleUp(api_key)

        assert hasattr(client, 'connection')
        assert isinstance(client.connection, Connection)
        assert client.connection._api_key == api_key

    def test_integration_resource(self, api_key):
        """Test integration resource is properly initialized."""
        client = BundleUp(api_key)

        assert hasattr(client, 'integration')
        assert isinstance(client.integration, Integration)
        assert client.integration._api_key == api_key

    def test_webhook_resource(self, api_key):
        """Test webhook resource is properly initialized."""
        client = BundleUp(api_key)

        assert hasattr(client, 'webhook')
        assert isinstance(client.webhook, Webhook)
        assert client.webhook._api_key == api_key
