"""
Credential manager.
see: https://developers.google.com/calendar/api/quickstart/python
"""

from pathlib import Path
from typing import List

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from showroomeventscheduler.google import DIRECTORY_GCP_SECRET
from showroomeventscheduler.google.token_manager import TokenManager


class CredentialManager:
    """Credential manager."""

    PATH_TO_CREDENTIALS = DIRECTORY_GCP_SECRET / "credentials.json"

    def __init__(self, scopes: List[str], *, path_to_credentials: Path = None, path_to_token: Path = None) -> None:
        self.token_manager = TokenManager(scopes, path_to_token=path_to_token)
        self.scopes = scopes
        self.path_to_credentials = self.PATH_TO_CREDENTIALS if path_to_credentials is None else path_to_credentials

    def create(self) -> Credentials:
        """
        The file token.json stores the user's access and refresh tokens,
        and is created automatically when the authorization flow completes for the first time.
        """
        creds = self.token_manager.load()
        if creds and creds.valid:
            # Reason: Can't define valid credentials in test.
            return creds  # pragma: no cover
        return self.login()

    def login(self) -> Credentials:
        """If there are no (valid) credentials available, let the user log in."""
        flow = InstalledAppFlow.from_client_secrets_file(self.path_to_credentials, self.scopes)
        creds = flow.run_local_server(port=0)
        self.token_manager.save(creds)
        return creds
