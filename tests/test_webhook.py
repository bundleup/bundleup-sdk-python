"""
Tests for the Webhook resource.
"""

import pytest
import responses
from bundleup.resources.webhook import Webhook


class TestWebhookInitialization:
    """Test Webhook resource initialization."""

    def test_init_with_api_key(self, api_key):
        """Test initialization with valid API key."""
        webhook = Webhook(api_key)

        assert webhook._api_key == api_key
        assert webhook._resource_name == "webhooks"

    def test_base_url(self, api_key):
        """Test base URL is correctly set."""
        webhook = Webhook(api_key)

        assert webhook.base_url == "https://api.bundleup.io"
        assert webhook.version == "v1"

    def test_connection_headers(self, api_key):
        """Test that connection headers are properly set."""
        webhook = Webhook(api_key)
        conn = webhook._connection

        assert conn.headers["Authorization"] == f"Bearer {api_key}"
        assert conn.headers["Content-Type"] == "application/json"


class TestWebhookList:
    """Test Webhook list method."""

    @responses.activate
    def test_list_webhooks(self, api_key):
        """Test listing all webhooks."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/webhooks/",
            json={
                "data": [
                    {
                        "id": "wh_1",
                        "url": "https://example.com/webhook1",
                        "events": ["connection.created"]
                    },
                    {
                        "id": "wh_2",
                        "url": "https://example.com/webhook2",
                        "events": ["connection.updated", "connection.deleted"]
                    }
                ]
            },
            status=200
        )

        webhook = Webhook(api_key)
        result = webhook.list()

        assert "data" in result
        data = result["data"]
        assert len(data) == 2
        assert data[0]["id"] == "wh_1"

    @responses.activate
    def test_list_webhooks_with_params(self, api_key):
        """Test listing webhooks with query parameters."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/webhooks/?status=active",
            json={"data": []},
            status=200
        )

        webhook = Webhook(api_key)
        result = webhook.list(params={"status": "active"})

        assert "data" in result
        assert result["data"] == []

    @responses.activate
    def test_list_webhooks_empty(self, api_key):
        """Test listing webhooks when none exist."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/webhooks/",
            json={"data": []},
            status=200
        )

        webhook = Webhook(api_key)
        result = webhook.list()

        assert "data" in result
        assert result["data"] == []


class TestWebhookCreate:
    """Test Webhook create method."""

    @responses.activate
    def test_create_webhook(self, api_key):
        """Test creating a new webhook."""
        webhook_data = {
            "url": "https://example.com/webhook",
            "events": ["connection.created", "connection.updated"]
        }

        responses.add(
            responses.POST,
            "https://api.bundleup.io/v1/webhooks/",
            json={
                "id": "wh_123",
                "url": webhook_data["url"],
                "events": webhook_data["events"],
                "status": "active"
            },
            status=201
        )

        webhook = Webhook(api_key)
        result = webhook.create(webhook_data)

        assert result["id"] == "wh_123"
        assert result["url"] == webhook_data["url"]
        assert result["events"] == webhook_data["events"]

    @responses.activate
    def test_create_webhook_with_secret(self, api_key):
        """Test creating a webhook with a secret."""
        webhook_data = {
            "url": "https://example.com/webhook",
            "events": ["connection.created"],
            "secret": "webhook_secret_123"
        }

        responses.add(
            responses.POST,
            "https://api.bundleup.io/v1/webhooks/",
            json={
                "id": "wh_123",
                "url": webhook_data["url"],
                "events": webhook_data["events"],
                "has_secret": True
            },
            status=201
        )

        webhook = Webhook(api_key)
        result = webhook.create(webhook_data)

        assert result["has_secret"] is True


class TestWebhookRetrieve:
    """Test Webhook retrieve method."""

    @responses.activate
    def test_retrieve_webhook(self, api_key, webhook_id):
        """Test retrieving a specific webhook."""
        responses.add(
            responses.GET,
            f"https://api.bundleup.io/v1/webhooks/{webhook_id}",
            json={
                "id": webhook_id,
                "url": "https://example.com/webhook",
                "events": ["connection.created"],
                "status": "active"
            },
            status=200
        )

        webhook = Webhook(api_key)
        result = webhook.retrieve(webhook_id)

        assert result["id"] == webhook_id

    def test_retrieve_webhook_without_id(self, api_key):
        """Test retrieving a webhook without ID raises ValueError."""
        webhook = Webhook(api_key)

        with pytest.raises(ValueError) as exc_info:
            webhook.retrieve(None)

        assert "ID is required for retrieval" in str(exc_info.value)

    @responses.activate
    def test_retrieve_webhook_not_found(self, api_key):
        """Test retrieving a non-existent webhook."""
        responses.add(
            responses.GET,
            "https://api.bundleup.io/v1/webhooks/nonexistent",
            json={"error": "Webhook not found"},
            status=404
        )

        webhook = Webhook(api_key)
        with pytest.raises(Exception) as exc_info:
            webhook.retrieve("nonexistent")

        assert "Failed to retrieve" in str(exc_info.value)
        assert "404" in str(exc_info.value)


class TestWebhookUpdate:
    """Test Webhook update method."""

    @responses.activate
    def test_update_webhook(self, api_key, webhook_id):
        """Test updating a webhook."""
        update_data = {
            "url": "https://example.com/new-webhook",
            "events": ["connection.created", "connection.updated", "connection.deleted"]
        }

        responses.add(
            responses.PUT,
            f"https://api.bundleup.io/v1/webhooks/{webhook_id}",
            json={
                "id": webhook_id,
                "url": update_data["url"],
                "events": update_data["events"]
            },
            status=200
        )

        webhook = Webhook(api_key)
        result = webhook.update(webhook_id, update_data)

        assert result["url"] == update_data["url"]
        assert len(result["events"]) == 3

    def test_update_webhook_without_id(self, api_key):
        """Test updating a webhook without ID raises ValueError."""
        webhook = Webhook(api_key)

        with pytest.raises(ValueError) as exc_info:
            webhook.update(None, {"url": "https://example.com"})

        assert "ID is required for update" in str(exc_info.value)

    @responses.activate
    def test_update_webhook_partial(self, api_key, webhook_id):
        """Test partially updating a webhook."""
        responses.add(
            responses.PUT,
            f"https://api.bundleup.io/v1/webhooks/{webhook_id}",
            json={
                "id": webhook_id,
                "url": "https://example.com/webhook",
                "events": ["connection.created"],
                "status": "inactive"
            },
            status=200
        )

        webhook = Webhook(api_key)
        result = webhook.update(webhook_id, {"status": "inactive"})

        assert result["status"] == "inactive"


class TestWebhookDelete:
    """Test Webhook delete method."""

    @responses.activate
    def test_delete_webhook(self, api_key, webhook_id):
        """Test deleting a webhook."""
        responses.add(
            responses.DELETE,
            f"https://api.bundleup.io/v1/webhooks/{webhook_id}",
            status=204
        )

        webhook = Webhook(api_key)
        result = webhook.delete(webhook_id)

        # 204 returns None
        assert result is None
        assert len(responses.calls) == 1

    def test_delete_webhook_without_id(self, api_key):
        """Test deleting a webhook without ID raises ValueError."""
        webhook = Webhook(api_key)

        with pytest.raises(ValueError) as exc_info:
            webhook.delete(None)

        assert "ID is required for deletion" in str(exc_info.value)

    @responses.activate
    def test_delete_webhook_not_found(self, api_key):
        """Test deleting a non-existent webhook."""
        responses.add(
            responses.DELETE,
            "https://api.bundleup.io/v1/webhooks/nonexistent",
            json={"error": "Webhook not found"},
            status=404
        )

        webhook = Webhook(api_key)
        with pytest.raises(Exception) as exc_info:
            webhook.delete("nonexistent")

        assert "Failed to delete" in str(exc_info.value)
        assert "404" in str(exc_info.value)


class TestWebhookURLBuilding:
    """Test URL building in Webhook resource."""

    def test_build_url_for_list(self, api_key):
        """Test building URL for list endpoint."""
        webhook = Webhook(api_key)
        url = webhook._build_url("")

        assert url == "https://api.bundleup.io/v1/webhooks/"

    def test_build_url_for_specific_resource(self, api_key, webhook_id):
        """Test building URL for specific resource."""
        webhook = Webhook(api_key)
        url = webhook._build_url(webhook_id)

        assert url == f"https://api.bundleup.io/v1/webhooks/{webhook_id}"
