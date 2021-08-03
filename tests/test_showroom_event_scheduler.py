"""Test for showroom_event_scheduler.py."""


class TestShowroomEventScheduler:
    """Test for ShowroomEventScheduler."""

    @staticmethod
    def test(network_and_file_mocked_showroom_event_scheduler):
        network_and_file_mocked_showroom_event_scheduler.run()
