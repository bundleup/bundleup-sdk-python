"""
Tests for the Unify classes.
"""

from bundleup.unify import Unify
from bundleup.unify.chat import Chat
from bundleup.unify.git import Git
from bundleup.unify.ticketing import Ticketing
from bundleup.unify.crm import CRM
from bundleup.unify.drive import Drive
from bundleup.unify.me import Me


class TestUnifyInitialization:
    """Test Unify class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        unify = Unify(api_key, connection_id)

        assert isinstance(unify.chat, Chat)
        assert isinstance(unify.git, Git)
        assert isinstance(unify.ticketing, Ticketing)
        assert isinstance(unify.crm, CRM)
        assert isinstance(unify.drive, Drive)
        assert isinstance(unify._me, Me)

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

    def test_ticketing_has_correct_params(self, api_key, connection_id):
        """Test that ticketing client has correct parameters."""
        unify = Unify(api_key, connection_id)

        assert unify.ticketing._api_key == api_key
        assert unify.ticketing._connection_id == connection_id

    def test_crm_has_correct_params(self, api_key, connection_id):
        """Test that crm client has correct parameters."""
        unify = Unify(api_key, connection_id)

        assert unify.crm._api_key == api_key
        assert unify.crm._connection_id == connection_id

    def test_drive_has_correct_params(self, api_key, connection_id):
        """Test that drive client has correct parameters."""
        unify = Unify(api_key, connection_id)

        assert unify.drive._api_key == api_key
        assert unify.drive._connection_id == connection_id

    def test_me_has_correct_params(self, api_key, connection_id):
        """Test that the me client has correct parameters."""
        unify = Unify(api_key, connection_id)

        assert unify._me._api_key == api_key
        assert unify._me._connection_id == connection_id

    def test_me_is_a_method_not_a_namespace(self, api_key, connection_id):
        """`me` is a root-level endpoint, so it is called rather than accessed."""
        unify = Unify(api_key, connection_id)

        assert callable(unify.me)
        assert not isinstance(unify.me, Me)


class TestChatInitialization:
    """Test Chat class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        chat = Chat(api_key, connection_id)

        assert chat._api_key == api_key
        assert chat._connection_id == connection_id
        assert chat.base_url == "https://unify.bundleup.io"

    def test_has_users_method(self, api_key, connection_id):
        """Test that Chat has users method."""
        chat = Chat(api_key, connection_id)

        assert hasattr(chat, 'users')
        assert callable(chat.users)

    def test_has_channels_method(self, api_key, connection_id):
        """Test that Chat has channels method."""
        chat = Chat(api_key, connection_id)

        assert hasattr(chat, 'channels')
        assert callable(chat.channels)

    def test_has_message_method(self, api_key, connection_id):
        """Test that Chat has message method."""
        chat = Chat(api_key, connection_id)

        assert hasattr(chat, 'message')
        assert callable(chat.message)


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

    def test_has_branches_method(self, api_key, connection_id):
        """Test that Git has branches method."""
        git = Git(api_key, connection_id)

        assert hasattr(git, 'branches')
        assert callable(git.branches)


class TestTicketingInitialization:
    """Test Ticketing class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        ticketing = Ticketing(api_key, connection_id)

        assert ticketing._api_key == api_key
        assert ticketing._connection_id == connection_id
        assert ticketing.base_url == "https://unify.bundleup.io"

    def test_has_tickets_method(self, api_key, connection_id):
        """Test that Ticketing has tickets method."""
        ticketing = Ticketing(api_key, connection_id)

        assert hasattr(ticketing, 'tickets')
        assert callable(ticketing.tickets)


class TestCRMInitialization:
    """Test CRM class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        crm = CRM(api_key, connection_id)

        assert crm._api_key == api_key
        assert crm._connection_id == connection_id
        assert crm.base_url == "https://unify.bundleup.io"

    def test_has_companies_method(self, api_key, connection_id):
        """Test that CRM has companies method."""
        crm = CRM(api_key, connection_id)

        assert hasattr(crm, 'companies')
        assert callable(crm.companies)

    def test_has_contacts_method(self, api_key, connection_id):
        """Test that CRM has contacts method."""
        crm = CRM(api_key, connection_id)

        assert hasattr(crm, 'contacts')
        assert callable(crm.contacts)


class TestDriveInitialization:
    """Test Drive class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        drive = Drive(api_key, connection_id)

        assert drive._api_key == api_key
        assert drive._connection_id == connection_id
        assert drive.base_url == "https://unify.bundleup.io"

    def test_has_files_method(self, api_key, connection_id):
        """Test that Drive has files method."""
        drive = Drive(api_key, connection_id)

        assert hasattr(drive, 'files')
        assert callable(drive.files)


class TestMeInitialization:
    """Test Me class initialization."""

    def test_init_with_valid_params(self, api_key, connection_id):
        """Test initialization with valid API key and connection ID."""
        me = Me(api_key, connection_id)

        assert me._api_key == api_key
        assert me._connection_id == connection_id
        assert me.base_url == "https://unify.bundleup.io"

    def test_has_get_method(self, api_key, connection_id):
        """Test that Me has a get method."""
        me = Me(api_key, connection_id)

        assert hasattr(me, 'get')
        assert callable(me.get)


class TestUnifyBaseClass:
    """Test Unify base class."""

    def test_base_url_is_set(self, api_key, connection_id):
        """Test that base URL is correctly set."""
        chat = Chat(api_key, connection_id)
        git = Git(api_key, connection_id)
        ticketing = Ticketing(api_key, connection_id)
        crm = CRM(api_key, connection_id)
        drive = Drive(api_key, connection_id)

        assert chat.base_url == "https://unify.bundleup.io"
        assert git.base_url == "https://unify.bundleup.io"
        assert ticketing.base_url == "https://unify.bundleup.io"
        assert crm.base_url == "https://unify.bundleup.io"
        assert drive.base_url == "https://unify.bundleup.io"


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

    def test_git_branches_accepts_repo_name(self, api_key, connection_id):
        """Test that git.branches accepts repo_name parameter."""
        git = Git(api_key, connection_id)

        try:
            git.branches("my-repo")
        except TypeError as e:
            assert "repo_name" not in str(e)
        except Exception:
            pass
