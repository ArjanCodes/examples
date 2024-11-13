from events import clear_event_listeners, events, register_event


def test_register_event() -> None:
    clear_event_listeners()
    register_event("test", lambda _: None)
    assert "test" in events


def test_multiple_listeners_registered() -> None:
    clear_event_listeners()
    register_event("test", lambda _: None)
    register_event("test", lambda _: None)

    assert len(events["test"]) == 2
