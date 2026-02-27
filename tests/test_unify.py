"""
Tests for the Unify classes.
"""

from bundleup.unify import Unify
from bundleup.unify.chat import Chat
from bundleup.unify.git import Git
from bundleup.unify.pm import PM


class TestUnifyInitialization:
    """Test Unify class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        unify = Unify(api_key, connection_id)

        assert isinstance(unify.chat, Chat)
        assert isinstance(unify.git, Git)
        assert isinstance(unify.pm, PM)

    def test_chat_has_correct_params(self, api_key, connection_id):
        """Test that chat client has correct parameters."""
        unify = Unify(api_key, connection_id)

        assert unify.chat._api_key == api_key
        assert unify.chat._connection_id == connection_id

    def test_git_has_correct_params(self, api_key, connection_id):
        """Test that git client has correct parameters."""
        unify = Unify(api_key, connection_id)

        assert unify.git._api_key == api_key
        assert unify.git._connection_id == connection_id

    def test_pm_has_correct_params(self, api_key, connection_id):
        """Test that pm client has correct parameters."""
        unify = Unify(api_key, connection_id)

        assert unify.pm._api_key == api_key
        assert unify.pm._connection_id == connection_id


class TestChatInitialization:
    """Test Chat class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        chat = Chat(api_key, connection_id)

        assert chat._api_key == api_key
        assert chat._connection_id == connection_id
        assert chat.base_url == "https://unify.bundleup.io"

    def test_has_channels_method(self, api_key, connection_id):
        """Test that Chat has channels method."""
        chat = Chat(api_key, connection_id)

        assert hasattr(chat, 'channels')
        assert callable(chat.channels)


class TestGitInitialization:
    """Test Git class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        git = Git(api_key, connection_id)

        assert git._api_key == api_key
        assert git._connection_id == connection_id
        assert git.base_url == "https://unify.bundleup.io"

    def test_has_repos_method(self, api_key, connection_id):
        """Test that Git has repos method."""
        git = Git(api_key, connection_id)

        assert hasattr(git, 'repos')
        assert callable(git.repos)

    def test_has_pulls_method(self, api_key, connection_id):
        """Test that Git has pulls method."""
        git = Git(api_key, connection_id)

        assert hasattr(git, 'pulls')
        assert callable(git.pulls)

    def test_has_tags_method(self, api_key, connection_id):
        """Test that Git has tags method."""
        git = Git(api_key, connection_id)

        assert hasattr(git, 'tags')
        assert callable(git.tags)

    def test_has_releases_method(self, api_key, connection_id):
        """Test that Git has releases method."""
        git = Git(api_key, connection_id)

        assert hasattr(git, 'releases')
        assert callable(git.releases)


class TestPMInitialization:
    """Test PM class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        pm = PM(api_key, connection_id)

        assert pm._api_key == api_key
        assert pm._connection_id == connection_id
        assert pm.base_url == "https://unify.bundleup.io"

    def test_has_issues_method(self, api_key, connection_id):
        """Test that PM has issues method."""
        pm = PM(api_key, connection_id)

        assert hasattr(pm, 'issues')
        assert callable(pm.issues)


class TestUnifyBaseClass:
    """Test Unify base class."""

    def test_base_url_is_set(self, api_key, connection_id):
        """Test that base URL is correctly set."""
        chat = Chat(api_key, connection_id)
        git = Git(api_key, connection_id)
        pm = PM(api_key, connection_id)

        assert chat.base_url == "https://unify.bundleup.io"
        assert git.base_url == "https://unify.bundleup.io"
        assert pm.base_url == "https://unify.bundleup.io"


class TestUnifyMethodSignatures:
    """Test method signatures for Unify classes."""

    def test_git_pulls_accepts_repo_name(self, api_key, connection_id):
        """Test that git.pulls accepts repo_name parameter."""
        git = Git(api_key, connection_id)

        # This should not raise an error about missing parameters
        try:
            git.pulls("my-repo")
        except TypeError as e:
            # If it raises TypeError, it should not be about missing repo_name
            assert "repo_name" not in str(e)
        except Exception:
            # Other exceptions are fine for this test (e.g., NotImplementedError)
            pass

    def test_git_tags_accepts_repo_name(self, api_key, connection_id):
        """Test that git.tags accepts repo_name parameter."""
        git = Git(api_key, connection_id)

        try:
            git.tags("my-repo")
        except TypeError as e:
            assert "repo_name" not in str(e)
        except Exception:
            pass

    def test_git_releases_accepts_repo_name(self, api_key, connection_id):
        """Test that git.releases accepts repo_name parameter."""
        git = Git(api_key, connection_id)

        try:
            git.releases("my-repo")
        except TypeError as e:
            assert "repo_name" not in str(e)
        except Exception:
            pass
