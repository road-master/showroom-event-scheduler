"""Event manager."""
import datetime
from logging import getLogger

from googleapiclient.discovery import Resource, build

from showroomeventscheduler.google.calendar.event import Event


class EventManager:
    """Event manager."""

    def __init__(self, creds, calendar_id, *, http=None) -> None:
        self.service = ServiceFactory("calendar", "v3", credentials=creds, http=http).create()
        self.calendar_id = calendar_id
        self.logger = getLogger(__name__)

    def register(self, event: Event):
        # Reason: Meta programing is used. pylint: disable=no-member
        self.service.events().insert(calendarId=self.calendar_id, body=event.convert_to_body()).execute()

    def check(self):
        """Call the Calendar API"""
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        self.logger.debug("Getting the upcoming 10 events")
        events_result = (
            # Reason: Meta programing is used. pylint: disable=no-member
            self.service.events()
            .list(calendarId=self.calendar_id, timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime",)
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            self.logger.debug("No upcoming events found.")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            self.logger.debug("%s %s", start, event["summary"])


class ServiceFactory:
    """
    To mock HTTP request when test
    since argument of credentials and http are excluded in build method.
    """

    def __init__(self, service_name, version, *, credentials=None, http=None):
        self.service_name = service_name
        self.version = version
        self.credentials = credentials
        self.http = http

    def create(self) -> Resource:
        return (
            build(self.service_name, self.version, credentials=self.credentials)
            if self.http is None
            else build(self.service_name, self.version, http=self.http)
        )
