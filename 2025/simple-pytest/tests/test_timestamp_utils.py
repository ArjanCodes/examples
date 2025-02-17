from datetime import timedelta

from src.timestamp_utils import to_timestamp


def test_always_returns_string():
    assert isinstance(to_timestamp(timedelta(seconds=1)), str)


def test_negative_duration():
    assert to_timestamp(timedelta(seconds=-1)) == "00:00:00.000"


def test_large_durations():
    assert to_timestamp(timedelta(days=2, hours=5, minutes=30)) == "53:30:00.000"


def test_to_timestamp_one_hour_two_minutes_three_seconds():
    assert (
        to_timestamp(timedelta(hours=1, minutes=2, seconds=3, milliseconds=456))
        == "01:02:03.456"
    )


def test_to_timestamp_zero_time():
    assert (
        to_timestamp(timedelta(hours=0, minutes=0, seconds=0, milliseconds=0))
        == "00:00:00.000"
    )


def test_to_timestamp_one_millisecond():
    assert (
        to_timestamp(timedelta(hours=0, minutes=0, seconds=0, milliseconds=1))
        == "00:00:00.001"
    )


def test_to_timestamp_fifty_nine_seconds_nine_hundred_ninety_nine_milliseconds():
    assert (
        to_timestamp(timedelta(hours=0, minutes=0, seconds=59, milliseconds=999))
        == "00:00:59.999"
    )


def test_microsecond_rounding():
    assert (
        to_timestamp(timedelta(hours=0, minutes=0, seconds=0, microseconds=500))
        == "00:00:00.000"
    )
