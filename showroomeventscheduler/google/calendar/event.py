"""Model of Google Calendar event."""
from dataclasses import dataclass
from datetime import datetime

from showroomeventscheduler.google.calendar.datetime import GoogleCalendarDatetime


@dataclass
class Event:
    summary: str
    start: datetime
    end: datetime

    def convert_to_body(self):
        return {
            "summary": self.summary,
            "start": GoogleCalendarDatetime.convert_to_google_calendar_format(self.start),
            "end": GoogleCalendarDatetime.convert_to_google_calendar_format(self.end),
        }
