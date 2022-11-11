from functools import partial

import pytest

from ..functions.operations import ChannelNotFoundError, get_channel

MOCK_DB = "tests/mock_channels.db"
get_channel_mock = partial(get_channel, db_path=MOCK_DB)


def test_get_channel_success() -> None:
    channel = get_channel_mock("arjancodes")
    assert channel["name"] == "ArjanCodes"


def test_get_channel_fail() -> None:
    with pytest.raises(ChannelNotFoundError):
        get_channel_mock("arjancodes123")
