"""
Tests for the MCP transport.
"""

import json

import responses

from bundleup.mcp import MCP

MCP_URL = "https://mcp.bundleup.io"


class TestTransport:
    """The stateless transport surface."""

    def test_transport_returns_url_and_headers(self, api_key, connection_id):
        transport = MCP(api_key, connection_id).transport()

        assert transport["url"] == MCP_URL
        assert transport["headers"]["Authorization"] == f"Bearer {api_key}"
        assert transport["headers"]["BU-Connection-Id"] == connection_id
        assert transport["headers"]["Accept"] == "application/json, text/event-stream"

    def test_hosted_joins_key_and_connection(self, api_key, connection_id):
        hosted = MCP(api_key, connection_id).hosted()

        assert hosted == {"url": MCP_URL, "token": f"{api_key}.{connection_id}"}

    def test_post_sends_the_body_untouched(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.POST, MCP_URL, json={"ok": True})

        payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
        response = MCP(api_key, connection_id).post(payload)

        assert response.status_code == 200
        assert json.loads(mock_responses.calls[0].request.body)["method"] == "tools/list"

    def test_post_accepts_a_serialized_body(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.POST, MCP_URL, json={"ok": True})

        MCP(api_key, connection_id).post('{"jsonrpc":"2.0"}')

        assert mock_responses.calls[0].request.body == '{"jsonrpc":"2.0"}'

    def test_post_merges_extra_headers(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.POST, MCP_URL, json={})

        MCP(api_key, connection_id).post({}, {"Mcp-Session-Id": "sess_abc"})

        request = mock_responses.calls[0].request
        assert request.headers["Mcp-Session-Id"] == "sess_abc"
        assert request.headers["BU-Connection-Id"] == connection_id

    def test_post_does_not_raise_on_an_error_response(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.POST, MCP_URL, json={"code": "rate_limit"}, status=429)

        assert MCP(api_key, connection_id).post({}).status_code == 429

    def test_delete_ends_a_session(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.DELETE, MCP_URL, body="", status=204)

        MCP(api_key, connection_id).delete({"Mcp-Session-Id": "sess_abc"})

        assert mock_responses.calls[0].request.headers["Mcp-Session-Id"] == "sess_abc"
