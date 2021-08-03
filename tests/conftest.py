"""Configuration of pytest"""
import shutil

import pytest
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import HttpMockSequence

from showroomeventscheduler.showroom_event_scheduler import ShowroomEventScheduler

SCOPES_FOR_TEST = ["https://www.googleapis.com/auth/calendar.events.owned"]


@pytest.fixture
def path_to_credentials_in_temp_path(tmp_path, resource_path_root):
    file_name_credentials_json = "credentials.json"
    path = tmp_path / file_name_credentials_json
    shutil.copy(resource_path_root / file_name_credentials_json, path)
    yield path


@pytest.fixture
def path_to_token_refreshed(resource_path_root):
    yield resource_path_root / "token_refreshed.json"


@pytest.fixture
def path_to_token_logined(resource_path_root):
    yield resource_path_root / "token_logined.json"


@pytest.fixture
def path_to_token_in_temp_path(tmp_path):
    yield tmp_path / "token.json"


@pytest.fixture
# Reason: pyrest fixture. pylint: disable=redefined-outer-name
def credentials_when_login(path_to_token_logined, path_to_token_in_temp_path, mocker):
    """
    Mocks method: InstalledAppFlow.run_local_server().
    Method to_json() returns:
    - string of path_to_token_in_temp_path.read_text() in case when run_local_server() hasn't been called,
    - string of token_logined.json in case when run_local_server() has been called.
    """
    credentials = Credentials.from_authorized_user_file(path_to_token_logined, SCOPES_FOR_TEST)
    mock = mocker.MagicMock(return_value=credentials)
    InstalledAppFlow.run_local_server = mock

    def mock_to_json() -> str:
        try:
            mock.assert_called_once_with(port=0)
        except AssertionError:
            return path_to_token_in_temp_path.read_text()
        else:
            return path_to_token_logined.read_text()

    mocker.patch.object(credentials, "to_json", mock_to_json)
    yield credentials


@pytest.fixture
# Reason: pyrest fixture. pylint: disable=redefined-outer-name
def credentials_when_refresh(mocker, resource_path_root, path_to_token_refreshed, path_to_token_in_temp_path):
    """
    Mocks method: Credentials.refresh(Request()).
    Method to_json() returns:
    - string of path_to_token_in_temp_path.read_text() in case when refresh() hasn't been called,
    - string of token_refreshed.json in case when refresh() has been called.
    """
    path_to_token_expired = resource_path_root / "token_expired.json"
    shutil.copy(path_to_token_expired, path_to_token_in_temp_path)
    credentials = Credentials.from_authorized_user_file(path_to_token_in_temp_path, SCOPES_FOR_TEST)
    credentials.refresh = mocker.MagicMock()

    def mock_to_json() -> str:
        try:
            credentials.refresh.assert_called_once()
            assert isinstance(credentials.refresh.call_args[0][0], Request)
        except AssertionError:
            return path_to_token_in_temp_path.read_text()
        else:
            return path_to_token_refreshed.read_text()

    mocker.patch.object(credentials, "to_json", mock_to_json)
    Credentials.from_authorized_user_file = mocker.MagicMock(return_value=credentials)
    yield credentials


@pytest.fixture
def http_mock_sequence(resource_path_root):
    response_event_insert = ({"status": "200"}, (resource_path_root / "event_insert_response.json").read_text())
    response_event_list = ({"status": "200"}, (resource_path_root / "event_list_response.json").read_text())
    return HttpMockSequence(([response_event_insert] * 15) + ([response_event_list] * 1))


@pytest.fixture
# Reason: pyrest fixture. pylint: disable=redefined-outer-name, unused-argument
def mock_credentials(credentials_when_refresh, credentials_when_login):
    pass


@pytest.fixture
# Reason: pyrest fixture. pylint: disable=redefined-outer-name, unused-argument
def network_and_file_mocked_showroom_event_scheduler(
    mock_credentials,
    path_to_credentials_in_temp_path,
    path_to_token_in_temp_path,
    resource_path_root,
    http_mock_sequence,
):
    """Serves network and filesystem closed ShowroomEventScheduler instance."""
    yield ShowroomEventScheduler(
        path_to_credentials=path_to_credentials_in_temp_path,
        path_to_token=path_to_token_in_temp_path,
        path_to_configuration=resource_path_root / "config.yml",
        http=http_mock_sequence,
    )
