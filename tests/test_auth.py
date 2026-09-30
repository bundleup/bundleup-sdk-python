"""
Tests for the Auth class.
"""

import json
from urllib.parse import parse_qs, urlparse

import pytest
import responses

from bundleup import BundleUp
from bundleup.auth import Auth

REDIRECT_URI = "https://app.example.com/callback"


class TestAuthAccessor:
    def test_exposed_on_client(self, api_key):
        client = BundleUp(api_key)

        assert isinstance(client.auth, Auth)
        assert client.auth is client.auth


class TestBuildAuthorizationUrl:
    def test_required_params(self, api_key):
        url = Auth(api_key).build_authorization_url("client_123", "github", REDIRECT_URI)
        parsed = urlparse(url)
        query = parse_qs(parsed.query)

        base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        assert base == "https://auth.bundleup.io/authorize"
        assert query["client_id"] == ["client_123"]
        assert query["integration_id"] == ["github"]
        assert query["redirect_uri"] == [REDIRECT_URI]
        assert "state" not in query
        assert "external_id" not in query

    def test_optional_params(self, api_key):
        url = Auth(api_key).build_authorization_url(
            "client_123", "github", REDIRECT_URI, external_id="user_42", state="xyz"
        )
        query = parse_qs(urlparse(url).query)

        assert query["external_id"] == ["user_42"]
        assert query["state"] == ["xyz"]

    @pytest.mark.parametrize(
        "args, message",
        [
            (("", "github", REDIRECT_URI), "client_id is required"),
            (("client_123", "", REDIRECT_URI), "integration_id is required"),
            (("client_123", "github", ""), "redirect_uri is required"),
        ],
    )
    def test_missing_required(self, api_key, args, message):
        with pytest.raises(ValueError, match=message):
            Auth(api_key).build_authorization_url(*args)


class TestGetConnectionFromCode:
    @responses.activate
    def test_exchanges_code(self, api_key):
        body = {"connection_id": "conn_1", "external_id": "user_42", "integration_id": "github"}
        responses.add(responses.POST, "https://auth.bundleup.io/connection", json=body, status=200)

        result = Auth(api_key).get_connection_from_code("code_abc", REDIRECT_URI)

        assert result == body
        request = responses.calls[0].request
        assert request.headers["Authorization"] == f"Bearer {api_key}"
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.body) == {"code": "code_abc", "redirect_uri": REDIRECT_URI}

    @responses.activate
    def test_error_includes_body(self, api_key):
        responses.add(
            responses.POST,
            "https://auth.bundleup.io/connection",
            json={"errors": {"code": ["Invalid or expired authorization code"]}},
            status=400,
        )

        with pytest.raises(Exception, match="400 - .*Invalid or expired authorization code"):
            Auth(api_key).get_connection_from_code("bad", REDIRECT_URI)

    def test_missing_code(self, api_key):
        with pytest.raises(ValueError, match="code is required"):
            Auth(api_key).get_connection_from_code("", REDIRECT_URI)

    def test_missing_redirect_uri(self, api_key):
        with pytest.raises(ValueError, match="redirect_uri is required"):
            Auth(api_key).get_connection_from_code("code_abc", "")
