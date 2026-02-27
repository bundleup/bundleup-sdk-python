"""
Tests for the Integration resource.
"""

import pytest
import responses
from bundleup.resources.integration import Integration


class TestIntegrationInitialization:
    """Test Integration resource initialization."""

    def test_init_with_api_key(self, api_key):
        """Test initialization with valid API key."""
        integration = Integration(api_key)

        assert integration._api_key == api_key
        assert integration._resource_name == "integrations"

    def test_base_url(self, api_key):
        """Test base URL is correctly set."""
        integration = Integration(api_key)

        assert integration.base_url == "https://api.bundleup.io"
        assert integration.version == "v1"

    def test_connection_headers(self, api_key):
        """Test that connection headers are properly set."""
        integration = Integration(api_key)
        conn = integration._connection

        assert conn.headers["Authorization"] == f"Bearer {api_key}"
        assert conn.headers["Content-Type"] == "application/json"


class TestIntegrationList:
    """Test Integration list method."""

    @responses.activate
    def test_list_integrations(self, api_key):
        """Test listing all integrations."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/integrations/",
            json={
                "data": [
                    {"id": "int_1", "name": "GitHub", "category": "git"},
                    {"id": "int_2", "name": "Slack", "category": "chat"}
                ]
            },
            status=200
        )

        integration = Integration(api_key)
        result = integration.list()

        assert "data" in result
        data = result["data"]
        assert len(data) == 2
        assert data[0]["name"] == "GitHub"

    @responses.activate
    def test_list_integrations_with_params(self, api_key):
        """Test listing integrations with query parameters."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/integrations/?category=git",
            json={"data": [{"id": "int_1", "name": "GitHub", "category": "git"}]},
            status=200
        )

        integration = Integration(api_key)
        result = integration.list(params={"category": "git"})

        assert "data" in result
        data = result["data"]
        assert len(data) == 1
        assert data[0]["category"] == "git"

    @responses.activate
    def test_list_integrations_empty(self, api_key):
        """Test listing integrations when none exist."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/integrations/",
            json={"data": []},
            status=200
        )

        integration = Integration(api_key)
        result = integration.list()

        assert "data" in result
        assert result["data"] == []


class TestIntegrationRetrieve:
    """Test Integration retrieve method."""

    @responses.activate
    def test_retrieve_integration(self, api_key, integration_id):
        """Test retrieving a specific integration."""
        responses.add(
            responses.GET,
            f"https://api.bundleup.io/v1/integrations/{integration_id}",
            json={
                "id": integration_id,
                "name": "GitHub",
                "category": "git",
                "auth_type": "oauth2"
            },
            status=200
        )

        integration = Integration(api_key)
        result = integration.retrieve(integration_id)

        assert result["id"] == integration_id
        assert result["name"] == "GitHub"

    def test_retrieve_integration_without_id(self, api_key):
        """Test retrieving an integration without ID raises ValueError."""
        integration = Integration(api_key)

        with pytest.raises(ValueError) as exc_info:
            integration.retrieve(None)

        assert "ID is required for retrieval" in str(exc_info.value)

    @responses.activate
    def test_retrieve_integration_not_found(self, api_key):
        """Test retrieving a non-existent integration."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/integrations/nonexistent",
            json={"error": "Integration not found"},
            status=404
        )

        integration = Integration(api_key)
        with pytest.raises(Exception) as exc_info:
            integration.retrieve("nonexistent")

        assert "Failed to retrieve" in str(exc_info.value)
        assert "404" in str(exc_info.value)


class TestIntegrationURLBuilding:
    """Test URL building in Integration resource."""

    def test_build_url_for_list(self, api_key):
        """Test building URL for list endpoint."""
        integration = Integration(api_key)
        url = integration._build_url("")

        assert url == "https://api.bundleup.io/v1/integrations/"

    def test_build_url_for_specific_resource(self, api_key, integration_id):
        """Test building URL for specific resource."""
        integration = Integration(api_key)
        url = integration._build_url(integration_id)

        assert url == f"https://api.bundleup.io/v1/integrations/{integration_id}"


class TestIntegrationAPIErrors:
    """Test Integration API error handling."""

    @responses.activate
    def test_unauthorized_request(self, api_key):
        """Test handling of unauthorized requests."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/integrations/",
            json={"error": "Unauthorized"},
            status=401
        )

        integration = Integration(api_key)
        with pytest.raises(Exception) as exc_info:
            integration.list()

        assert "Failed to fetch" in str(exc_info.value)
        assert "401" in str(exc_info.value)

    @responses.activate
    def test_server_error(self, api_key):
        """Test handling of server errors."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/integrations/",
            json={"error": "Internal server error"},
            status=500
        )

        integration = Integration(api_key)
        with pytest.raises(Exception) as exc_info:
            integration.list()

        assert "Failed to fetch" in str(exc_info.value)
        assert "500" in str(exc_info.value)
