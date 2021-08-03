"""Datetime for radiko specification."""
from datetime import datetime
from typing import Dict


class GoogleCalendarDatetime:
    """Datetime for Google Calendar specification."""

    @staticmethod
    def convert_to_google_calendar_format(datetime_jst: datetime) -> Dict[str, str]:
        return {
            "timeZone": "Asia/Tokyo",
            "dateTime": datetime_jst.isoformat(),
        }
