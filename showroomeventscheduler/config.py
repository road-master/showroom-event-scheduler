"""Configuration."""
from dataclasses import dataclass, field
from typing import Iterable, List

from dataclasses_json import DataClassJsonMixin
from yamldataclassconfig.config import YamlDataClassConfig

from showroomeventscheduler.datetime import ShowroomEventSchedulerDatetime
from showroomeventscheduler.showroom.live import Live


@dataclass
class Event(DataClassJsonMixin):
    """Model of event for loading YAML."""

    start: str
    end: str

    @property
    def start_datetime(self):
        return ShowroomEventSchedulerDatetime.parse_time_to_today(self.start)

    @property
    def end_datetime(self):
        return ShowroomEventSchedulerDatetime.parse_time_to_today(self.end)


@dataclass
class Config(YamlDataClassConfig):
    """Configuration."""

    calendar_id: str = None  # type: ignore
    summary: str = None  # type: ignore
    events: List[Event] = field(default_factory=list)

    @property
    def lives(self) -> Iterable[Live]:
        return (Live(event.start_datetime, event.end_datetime) for event in self.events)
