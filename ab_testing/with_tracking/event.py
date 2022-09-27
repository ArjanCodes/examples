import os

from mixpanel import Mixpanel


def post_event(event_type: str) -> None:
    token = os.getenv("MIXPANEL_TOKEN") or ""
    print(token)
    m_panel = Mixpanel(token)
    m_panel.track("ID", event_type)
