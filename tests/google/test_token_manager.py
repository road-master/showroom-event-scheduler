"""Test for token_manager.py"""
from google.oauth2.credentials import Credentials

from showroomeventscheduler.google.token_manager import TokenManager
from tests.conftest import SCOPES_FOR_TEST


class TestTokenManager:
    """Test for TokenManager"""

    @staticmethod
    def test_not_exist(path_to_token_in_temp_path):
        token_manager = TokenManager(SCOPES_FOR_TEST, path_to_token=path_to_token_in_temp_path)
        assert token_manager.load() is None

    @staticmethod
    def test_refresh(credentials_when_refresh, path_to_token_in_temp_path, path_to_token_refreshed):
        token_manager = TokenManager(SCOPES_FOR_TEST, path_to_token=path_to_token_in_temp_path)
        assert token_manager.load() == credentials_when_refresh
        # Reason: This is mocked in fixture. pylint: disable=no-member
        Credentials.from_authorized_user_file.assert_called_once_with(path_to_token_in_temp_path, SCOPES_FOR_TEST)
        assert path_to_token_in_temp_path.read_text() == path_to_token_refreshed.read_text()
