"""Datetime of SHOWROOM Event Scheduler."""
from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone

from dateutil.parser import parse


@dataclass
class ParsedTime:
    time: time
    date: int


class ShowroomEventSchedulerDatetime:
    """Datetime of SHOWROOM Event Scheduler."""

    @staticmethod
    def parse_time_to_today(time_string: str):
        parsed_date = ShowroomEventSchedulerDatetime.now_jst().date()
        parsed_time = ShowroomEventSchedulerDatetime.parse_time(time_string)
        calculated_date = parsed_date + timedelta(days=parsed_time.date)
        calculated_time = parsed_time.time
        return datetime.combine(calculated_date, calculated_time)

    @staticmethod
    def parse_time(time_string: str) -> ParsedTime:
        """time_string: like "23:53". """
        try:
            return ParsedTime(parse(time_string).time(), 0)
        except ValueError as error:
            if "hour must be in 0..23" not in str(error):
                raise error
        return ShowroomEventSchedulerDatetime.parse_time_over_24_hour(time_string)

    @staticmethod
    def parse_time_over_24_hour(time_string: str) -> ParsedTime:
        """Parses time which is over than 24 hour like "24:25"."""
        split_time = time_string.split(":")
        if len(split_time) != 2:
            raise ValueError(f"Invalid time format. {time_string=}")
        hour_string = split_time[0]
        time_string = split_time[1]
        hour_int = int(hour_string)
        day = hour_int // 24
        hour_in_24_hour = hour_int % 24
        return ParsedTime(parse(f"{hour_in_24_hour}:{time_string}").time(), day)

    @staticmethod
    def now_jst() -> datetime:
        return datetime.now(tz=timezone(timedelta(hours=+9), "JST"))
