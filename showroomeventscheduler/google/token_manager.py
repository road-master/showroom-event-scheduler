"""Token manager."""
from pathlib import Path
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from showroomeventscheduler.google import DIRECTORY_GCP_SECRET


class TokenManager:
    """Token manager."""

    PATH_TO_TOKEN = DIRECTORY_GCP_SECRET / "token.json"

    def __init__(self, scopes: List[str], *, path_to_token: Path = None):
        self.scopes = scopes
        self.path_to_token = self.PATH_TO_TOKEN if path_to_token is None else path_to_token

    def load(self) -> Optional[Credentials]:
        """Loads token."""
        if not self.path_to_token.exists():
            return None
        creds = Credentials.from_authorized_user_file(self.path_to_token, self.scopes)
        if creds.valid:
            # Reason: Can't define valid credentials in test.
            return creds  # pragma: no cover
        if creds.expired and creds.refresh_token:
            return self.refresh(creds)
            # Reason: Can't define credentials to run through this line.
        return None  # pragma: no cover

    def refresh(self, creds: Credentials) -> Credentials:
        creds.refresh(Request())
        self.save(creds)
        return creds

    def save(self, creds: Credentials) -> None:
        """Save the credentials for the next run"""
        self.path_to_token.write_text(creds.to_json())
