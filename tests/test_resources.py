"""Tests for resource classes."""

import pytest
from bundleup.connection import Connections
from bundleup.integration import Integrations
from bundleup.webhooks import Webhooks


def test_connections_namespace():
    """Test Connections namespace."""
    conn = Connections("test-api-key")
    assert conn._namespace == "connections"


def test_integrations_namespace():
    """Test Integrations namespace."""
    integ = Integrations("test-api-key")
    assert integ._namespace == "integrations"


def test_webhooks_namespace():
    """Test Webhooks namespace."""
    hooks = Webhooks("test-api-key")
    assert hooks._namespace == "webhooks"
