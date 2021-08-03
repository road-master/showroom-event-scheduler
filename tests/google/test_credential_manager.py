"""Test for credential_manager.py."""
from google_auth_oauthlib.flow import InstalledAppFlow

from showroomeventscheduler.google.credential_manager import CredentialManager
from tests.conftest import SCOPES_FOR_TEST


class TestCredentialManager:
    """Test for CredentialManager."""

    @staticmethod
    def test(
        path_to_token_logined, credentials_when_login, path_to_credentials_in_temp_path, path_to_token_in_temp_path,
    ):
        """
        - Credential instance should be created.
        - Login page should be displayed.
        - Token file should be created.
        """
        cred = CredentialManager(
            SCOPES_FOR_TEST,
            path_to_credentials=path_to_credentials_in_temp_path,
            path_to_token=path_to_token_in_temp_path,
        ).create()
        assert cred == credentials_when_login
        # Reason: This is mocked in fixture. pylint: disable=no-member
        InstalledAppFlow.run_local_server.assert_called_once_with(port=0)
        assert path_to_token_in_temp_path.read_text() == path_to_token_logined.read_text()
