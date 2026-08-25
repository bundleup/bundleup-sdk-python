"""
Tests for the MCP transport and managed client.
"""

import json

import pytest
import responses

from bundleup.mcp import MCP, MCPClient
from bundleup.unify.mcp import MCP as UnifiedMCP

MCP_URL = "https://mcp.bundleup.io"
UNIFY_MCP_URL = "https://unify.bundleup.io/v1/mcp"

TOOL = {
    "name": "create_issue",
    "description": "Create an issue",
    "inputSchema": {"type": "object"},
}


def rpc(message_id, result=None, error=None):
    """A JSON-RPC response body."""
    payload = {"jsonrpc": "2.0", "id": message_id}

    if error is not None:
        payload["error"] = error
    else:
        payload["result"] = result or {}

    return payload


def add_handshake(mock, url=MCP_URL, session_id="sess_123"):
    """initialize, then notifications/initialized."""
    mock.add(
        responses.POST,
        url,
        json=rpc(1, {"protocolVersion": "2025-06-18"}),
        headers={"Mcp-Session-Id": session_id},
    )
    mock.add(responses.POST, url, body="", status=202)


def bodies(mock):
    return [json.loads(call.request.body) for call in mock.calls if call.request.body]


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

    def test_connect_returns_managed_client(self, api_key, connection_id):
        assert isinstance(MCP(api_key, connection_id).connect(), MCPClient)

    def test_connect_returns_a_new_client_each_call(self, api_key, connection_id):
        mcp = MCP(api_key, connection_id)

        assert mcp.connect() is not mcp.connect()

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


class TestHandshake:
    """The managed client's lazy handshake."""

    def test_handshakes_before_the_first_call(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses)
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, {"tools": [TOOL]}))

        MCP(api_key, connection_id).connect().list_tools()

        sent = bodies(mock_responses)
        assert [message["method"] for message in sent] == [
            "initialize",
            "notifications/initialized",
            "tools/list",
        ]
        assert "id" not in sent[1]

    def test_handshakes_only_once(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses)
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, {"tools": []}))
        mock_responses.add(responses.POST, MCP_URL, json=rpc(3, {"resources": []}))

        client = MCP(api_key, connection_id).connect()
        client.list_tools()
        client.list_resources()

        assert sum(1 for m in bodies(mock_responses) if m["method"] == "initialize") == 1

    def test_replays_the_session_id(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses, session_id="sess_abc")
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, {"tools": []}))

        MCP(api_key, connection_id).connect().list_tools()

        assert "Mcp-Session-Id" not in mock_responses.calls[0].request.headers
        assert mock_responses.calls[2].request.headers["Mcp-Session-Id"] == "sess_abc"

    def test_retries_the_handshake_after_a_failure(self, api_key, connection_id, mock_responses):
        mock_responses.add(
            responses.POST,
            MCP_URL,
            json={"code": "rate_limit", "message": "Too many requests"},
            status=429,
        )
        client = MCP(api_key, connection_id).connect()

        with pytest.raises(Exception, match="Too many requests"):
            client.list_tools()

        add_handshake(mock_responses)
        mock_responses.add(responses.POST, MCP_URL, json=rpc(3, {"tools": [TOOL]}))

        assert client.list_tools() == [TOOL]


class TestTools:
    """Listing and calling tools."""

    def test_returns_the_provider_tool_list(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses)
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, {"tools": [TOOL]}))

        assert MCP(api_key, connection_id).connect().list_tools() == [TOOL]

    def test_follows_pagination(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses)
        page_one = rpc(2, {"tools": [TOOL], "nextCursor": "page2"})
        page_two = rpc(3, {"tools": [{**TOOL, "name": "list_issues"}]})
        mock_responses.add(responses.POST, MCP_URL, json=page_one)
        mock_responses.add(responses.POST, MCP_URL, json=page_two)

        tools = MCP(api_key, connection_id).connect().list_tools()

        assert len(tools) == 2
        assert bodies(mock_responses)[3]["params"] == {"cursor": "page2"}

    def test_parses_an_event_stream_response(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses)
        stream = (
            'event: message\r\ndata: {"jsonrpc":"2.0","method":"notifications/message"}\r\n\r\n'
            'event: message\r\ndata: {"jsonrpc":"2.0","id":2,"result":{"tools":['
            + json.dumps(TOOL)
            + ']}}\r\n\r\n'
        )
        mock_responses.add(
            responses.POST,
            MCP_URL,
            body=stream,
            content_type="text/event-stream",
        )

        assert MCP(api_key, connection_id).connect().list_tools() == [TOOL]

    def test_calls_a_tool(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses)
        content = {"content": [{"type": "text", "text": "done"}]}
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, content))

        client = MCP(api_key, connection_id).connect()
        result = client.call_tool("create_issue", {"title": "Login broken"})

        assert result["content"][0]["text"] == "done"
        assert bodies(mock_responses)[2]["params"] == {
            "name": "create_issue",
            "arguments": {"title": "Login broken"},
        }

    def test_requires_a_tool_name(self, api_key, connection_id):
        with pytest.raises(ValueError, match="Tool name is required"):
            MCP(api_key, connection_id).connect().call_tool("")

    def test_surfaces_a_json_rpc_error(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses)
        failure = rpc(2, error={"code": -32602, "message": "Unknown tool"})
        mock_responses.add(responses.POST, MCP_URL, json=failure)

        with pytest.raises(Exception, match="Unknown tool"):
            MCP(api_key, connection_id).connect().call_tool("nope")


class TestResourcesAndPrompts:
    """The rest of the protocol surface."""

    def test_lists_resources(self, api_key, connection_id, mock_responses):
        resource = {"uri": "file:///readme.md", "name": "readme"}
        add_handshake(mock_responses)
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, {"resources": [resource]}))

        assert MCP(api_key, connection_id).connect().list_resources() == [resource]

    def test_reads_a_resource(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses)
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, {"contents": []}))

        MCP(api_key, connection_id).connect().read_resource("file:///readme.md")

        assert bodies(mock_responses)[2]["params"] == {"uri": "file:///readme.md"}

    def test_requires_a_resource_uri(self, api_key, connection_id):
        with pytest.raises(ValueError, match="Resource URI is required"):
            MCP(api_key, connection_id).connect().read_resource("")

    def test_lists_prompts(self, api_key, connection_id, mock_responses):
        prompt = {"name": "summarize"}
        add_handshake(mock_responses)
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, {"prompts": [prompt]}))

        assert MCP(api_key, connection_id).connect().list_prompts() == [prompt]

    def test_gets_a_prompt(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses)
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, {"messages": []}))

        MCP(api_key, connection_id).connect().get_prompt("summarize", {"id": "1"})

        expected = {"name": "summarize", "arguments": {"id": "1"}}
        assert bodies(mock_responses)[2]["params"] == expected

    def test_requires_a_prompt_name(self, api_key, connection_id):
        with pytest.raises(ValueError, match="Prompt name is required"):
            MCP(api_key, connection_id).connect().get_prompt("")

    def test_sends_an_arbitrary_method(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses)
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, {"ok": True}))

        client = MCP(api_key, connection_id).connect()

        assert client.request("logging/setLevel", {"level": "debug"}) == {"ok": True}

    def test_requires_a_method(self, api_key, connection_id):
        with pytest.raises(ValueError, match="Method is required"):
            MCP(api_key, connection_id).connect().request("")


class TestErrors:
    """BundleUp rejections, which are HTTP responses rather than JSON-RPC."""

    def test_includes_the_error_code(self, api_key, connection_id, mock_responses):
        mock_responses.add(
            responses.POST,
            MCP_URL,
            json={
                "status": 400,
                "code": "connection_invalid",
                "message": "Missing or invalid connection ID",
            },
            status=400,
        )

        expected = r"Missing or invalid connection ID \(connection_invalid\)"

        with pytest.raises(Exception, match=expected):
            MCP(api_key, connection_id).connect().list_tools()

    def test_falls_back_to_the_status(self, api_key, connection_id, mock_responses):
        mock_responses.add(responses.POST, MCP_URL, body="gateway timeout", status=504)

        with pytest.raises(Exception, match="MCP request failed with status 504."):
            MCP(api_key, connection_id).connect().list_tools()


class TestClose:
    """Ending a session."""

    def test_deletes_the_session(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses, session_id="sess_xyz")
        mock_responses.add(responses.POST, MCP_URL, json=rpc(2, {"tools": []}))
        mock_responses.add(responses.DELETE, MCP_URL, body="", status=204)

        client = MCP(api_key, connection_id).connect()
        client.list_tools()
        client.close()

        assert mock_responses.calls[-1].request.method == "DELETE"
        assert mock_responses.calls[-1].request.headers["Mcp-Session-Id"] == "sess_xyz"

    def test_does_not_delete_without_a_session(self, api_key, connection_id, mock_responses):
        MCP(api_key, connection_id).connect().close()

        assert len(mock_responses.calls) == 0


class TestUnifiedMCP:
    """Unified MCP targets BundleUp's own normalized tools."""

    def test_hosted_targets_the_unified_server(self, api_key, connection_id):
        assert UnifiedMCP(api_key, connection_id).hosted() == {
            "url": UNIFY_MCP_URL,
            "token": f"{api_key}.{connection_id}",
        }

    def test_lists_tools_against_the_unified_server(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses, url=UNIFY_MCP_URL)
        mock_responses.add(responses.POST, UNIFY_MCP_URL, json=rpc(2, {"tools": [TOOL]}))

        assert UnifiedMCP(api_key, connection_id).list_tools() == [TOOL]
        assert all(call.request.url.startswith(UNIFY_MCP_URL) for call in mock_responses.calls)

    def test_calls_a_tool(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses, url=UNIFY_MCP_URL)
        mock_responses.add(responses.POST, UNIFY_MCP_URL, json=rpc(2, {"content": []}))

        UnifiedMCP(api_key, connection_id).call_tool("send_message", {"text": "hi"})

        assert bodies(mock_responses)[2]["params"] == {
            "name": "send_message",
            "arguments": {"text": "hi"},
        }

    def test_requires_a_tool_name(self, api_key, connection_id):
        with pytest.raises(ValueError, match="Tool name is required"):
            UnifiedMCP(api_key, connection_id).call_tool("")

    def test_reuses_one_session_across_calls(self, api_key, connection_id, mock_responses):
        add_handshake(mock_responses, url=UNIFY_MCP_URL)
        mock_responses.add(responses.POST, UNIFY_MCP_URL, json=rpc(2, {"tools": []}))
        mock_responses.add(responses.POST, UNIFY_MCP_URL, json=rpc(3, {"content": []}))

        unified = UnifiedMCP(api_key, connection_id)
        unified.list_tools()
        unified.call_tool("send_message")

        assert sum(1 for m in bodies(mock_responses) if m["method"] == "initialize") == 1
