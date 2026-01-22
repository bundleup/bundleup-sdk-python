"""Tests for the Unify API."""

import pytest
import responses
from bundleup.unify import Unify
from bundleup.unify.chat import Chat
from bundleup.unify.git import Git
from bundleup.unify.pm import PM


def test_unify_init():
    """Test Unify initialization."""
    unify = Unify("test-api-key", "connection-id")
    assert unify._api_key == "test-api-key"
    assert unify._connection_id == "connection-id"


def test_unify_chat_property():
    """Test chat property returns Chat instance."""
    unify = Unify("test-api-key", "connection-id")
    assert isinstance(unify.chat, Chat)


def test_unify_git_property():
    """Test git property returns Git instance."""
    unify = Unify("test-api-key", "connection-id")
    assert isinstance(unify.git, Git)


def test_unify_pm_property():
    """Test pm property returns PM instance."""
    unify = Unify("test-api-key", "connection-id")
    assert isinstance(unify.pm, PM)


@responses.activate
def test_chat_channels():
    """Test Chat.channels method."""
    responses.add(
        responses.GET,
        "https://unify.bundleup.io/chat/channels",
        json={
            "data": [{"id": "1", "name": "general"}],
            "_raw": None,
            "metadata": {"has_more": False, "next_cursor": None}
        },
        status=200
    )
    
    chat = Chat("test-api-key", "connection-id")
    result = chat.channels()
    assert len(result["data"]) == 1
    assert result["data"][0]["name"] == "general"


@responses.activate
def test_chat_channels_with_params():
    """Test Chat.channels with parameters."""
    responses.add(
        responses.GET,
        "https://unify.bundleup.io/chat/channels",
        json={
            "data": [{"id": "1", "name": "general"}],
            "_raw": [{"original": "data"}],
            "metadata": {"has_more": True, "next_cursor": "cursor123"}
        },
        status=200
    )
    
    chat = Chat("test-api-key", "connection-id")
    result = chat.channels({"limit": 10, "include_raw": True})
    assert result["metadata"]["has_more"] is True


@responses.activate
def test_git_repos():
    """Test Git.repos method."""
    responses.add(
        responses.GET,
        "https://unify.bundleup.io/git/repos",
        json={
            "data": [{"id": "1", "name": "my-repo"}],
            "_raw": None,
            "metadata": {"has_more": False, "next_cursor": None}
        },
        status=200
    )
    
    git = Git("test-api-key", "connection-id")
    result = git.repos()
    assert len(result["data"]) == 1
    assert result["data"][0]["name"] == "my-repo"


@responses.activate
def test_git_pulls():
    """Test Git.pulls method."""
    responses.add(
        responses.GET,
        "https://unify.bundleup.io/git/pulls",
        json={
            "data": [{"id": "1", "title": "PR title"}],
            "_raw": None,
            "metadata": {"has_more": False, "next_cursor": None}
        },
        status=200
    )
    
    git = Git("test-api-key", "connection-id")
    result = git.pulls()
    assert len(result["data"]) == 1


@responses.activate
def test_git_tags():
    """Test Git.tags method."""
    responses.add(
        responses.GET,
        "https://unify.bundleup.io/git/tags",
        json={
            "data": [{"id": "1", "name": "v1.0.0"}],
            "_raw": None,
            "metadata": {"has_more": False, "next_cursor": None}
        },
        status=200
    )
    
    git = Git("test-api-key", "connection-id")
    result = git.tags()
    assert len(result["data"]) == 1


@responses.activate
def test_git_releases():
    """Test Git.releases method."""
    responses.add(
        responses.GET,
        "https://unify.bundleup.io/git/releases",
        json={
            "data": [{"id": "1", "tag": "v1.0.0"}],
            "_raw": None,
            "metadata": {"has_more": False, "next_cursor": None}
        },
        status=200
    )
    
    git = Git("test-api-key", "connection-id")
    result = git.releases()
    assert len(result["data"]) == 1


@responses.activate
def test_pm_issues():
    """Test PM.issues method."""
    responses.add(
        responses.GET,
        "https://unify.bundleup.io/pm/issues",
        json={
            "data": [{"id": "1", "title": "Bug fix"}],
            "_raw": None,
            "metadata": {"has_more": False, "next_cursor": None}
        },
        status=200
    )
    
    pm = PM("test-api-key", "connection-id")
    result = pm.issues()
    assert len(result["data"]) == 1
    assert result["data"][0]["title"] == "Bug fix"
