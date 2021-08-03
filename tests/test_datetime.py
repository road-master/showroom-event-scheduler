"""Test for datetime.py."""
import pytest

from showroomeventscheduler.datetime import ShowroomEventSchedulerDatetime


class TestShowroomEventSchedulerDatetime:
    """Test for ShowroomEventSchedulerDatetime."""

    @staticmethod
    def test_parse_time_over_24_hour():
        with pytest.raises(ValueError):
            ShowroomEventSchedulerDatetime.parse_time_over_24_hour("23:25:30")

    @staticmethod
    def test_parse_time():
        with pytest.raises(ValueError):
            ShowroomEventSchedulerDatetime.parse_time("??:??")
