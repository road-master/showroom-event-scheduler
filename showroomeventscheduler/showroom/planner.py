"""Planner."""
from datetime import datetime, timedelta
from typing import Iterable, List

from showroomeventscheduler.google.calendar.event import Event
from showroomeventscheduler.showroom.live import Live


class Planner:
    """Planner."""

    def __init__(self, summary: str, list_live: Iterable[Live]) -> None:
        self.summary = summary
        self.list_live = list_live

    def plan(self) -> List[Event]:
        list_event: List[Event] = []
        for live in self.list_live:
            list_event.append(self.create_event_spend_star(live))
            list_event.append(self.create_event_interval_starting_collecting_star(live))
            list_event.append(self.create_event_live(live))
        return list_event

    def create_event_spend_star(self, live: Live) -> Event:
        return Event("捨て星", self.calculate_start_time_spend_star(live), self.calculate_end_time_spend_star(live),)

    def create_event_interval_starting_collecting_star(self, live: Live) -> Event:
        return Event(
            "星集め開始禁止時間",
            self.calculate_start_time_interval_starting_collecting_star(live),
            self.calculate_end_time_interval_starting_collecting_star(live),
        )

    def create_event_live(self, live: Live) -> Event:
        return Event(self.summary, live.start, live.end)

    @staticmethod
    def calculate_start_time_spend_star(live: Live) -> datetime:
        return live.start - timedelta(minutes=45)

    @staticmethod
    def calculate_end_time_spend_star(live: Live) -> datetime:
        return live.end - timedelta(hours=1)

    def calculate_start_time_interval_starting_collecting_star(self, live: Live) -> datetime:
        return self.calculate_end_time_spend_star(live) - timedelta(hours=1)

    @staticmethod
    def calculate_end_time_interval_starting_collecting_star(live: Live) -> datetime:
        return live.start - timedelta(minutes=55)
