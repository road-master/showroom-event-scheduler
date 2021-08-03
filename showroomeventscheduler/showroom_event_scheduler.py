"""SHOWROOM Event Schediler"""
from pathlib import Path

from showroomeventscheduler import CONFIG
from showroomeventscheduler.google.calendar.event_manager import EventManager
from showroomeventscheduler.google.credential_manager import CredentialManager
from showroomeventscheduler.showroom.planner import Planner


class ShowroomEventScheduler:
    """SHOWROOM Event Scheduler"""

    def __init__(
        self,
        *,
        path_to_credentials: Path = None,
        path_to_token: Path = None,
        path_to_configuration: Path = None,
        http=None
    ) -> None:
        # If modifying these scopes, delete the file token.json.
        self.scopes = ["https://www.googleapis.com/auth/calendar.events.owned"]
        self.credential_manager = CredentialManager(
            self.scopes, path_to_credentials=path_to_credentials, path_to_token=path_to_token
        )
        self.http = http
        CONFIG.load(path_to_configuration)

    def run(self):
        """
        Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = self.credential_manager.create()
        list_event = Planner(CONFIG.summary, CONFIG.lives).plan()
        event_manager = EventManager(creds, CONFIG.calendar_id, http=self.http)
        for event in list_event:
            event_manager.register(event)
        event_manager.check()
