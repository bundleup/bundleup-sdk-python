"""
Pytest configuration and shared fixtures for BundleUp SDK tests.
"""

import pytest
import responses


@pytest.fixture
def api_key():
    """Return a test API key."""
    return "test_api_key_12345"


@pytest.fixture
def connection_id():
    """Return a test connection ID."""
    return "conn_test123"


@pytest.fixture
def integration_id():
    """Return a test integration ID."""
    return "int_test123"


@pytest.fixture
def webhook_id():
    """Return a test webhook ID."""
    return "wh_test123"


@pytest.fixture
def mock_responses():
    """Activate responses mock for HTTP requests."""
    with responses.RequestsMock() as rsps:
        yield rsps
