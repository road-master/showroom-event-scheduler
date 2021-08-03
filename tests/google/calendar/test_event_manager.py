"""Test for event_manager.py."""
from datetime import datetime, timedelta, timezone

from googleapiclient.http import HttpMock

from showroomeventscheduler.google.calendar.event import Event
from showroomeventscheduler.google.calendar.event_manager import EventManager


class TestEventManager:
    """Test for EventManager."""

    @staticmethod
    def test_register(resource_path_root):
        """Smoke test."""
        creds = None
        calendar_id = "calendar_id"
        http = HttpMock(filename=(resource_path_root / "event_insert_response.json"), headers={"status": "200"},)
        event_manager = EventManager(creds, calendar_id, http=http)
        event = Event(
            "test",
            datetime(2021, 7, 22, 23, 55, 0, 0, timezone(timedelta(hours=+9), "JST")),
            datetime(2021, 7, 23, 0, 25, 0, 0, timezone(timedelta(hours=+9), "JST")),
        )
        event_manager.register(event)

    @staticmethod
    def test_check(resource_path_root):
        creds = None
        calendar_id = "calendar_id"
        http = HttpMock(filename=(resource_path_root / "event_list_response.json"), headers={"status": "200"},)
        event_manager = EventManager(creds, calendar_id, http=http)
        event_manager.check()

    @staticmethod
    def test_check_empty(resource_path_root):
        creds = None
        calendar_id = "calendar_id"
        http = HttpMock(filename=(resource_path_root / "event_list_response_empty.json"), headers={"status": "200"},)
        event_manager = EventManager(creds, calendar_id, http=http)
        event_manager.check()
