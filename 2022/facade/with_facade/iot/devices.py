class HueLightDevice:
    def connect(self) -> None:
        print("Connecting Hue light.")

    def disconnect(self) -> None:
        print("Disconnecting Hue light.")

    def status_update(self) -> str:
        return "hue_light_status_ok"

    def connection_info(self) -> tuple[str, int]:
        return "192.168.1.100", 1234


class SmartSpeakerDevice:
    def connect(self) -> None:
        print("Connecting to Smart Speaker.")

    def disconnect(self) -> None:
        print("Disconnecting Smart Speaker.")

    def status_update(self) -> str:
        return "smart_speaker_status_ok"

    def connection_info(self) -> tuple[str, int]:
        return "192.168.1.101", 2368


class CurtainsDevice:
    def connect(self) -> None:
        print("Connecting to Curtains.")

    def disconnect(self) -> None:
        print("Disconnecting Curtains.")

    def status_update(self) -> str:
        return "curtains_status_ok"

    def connection_info(self) -> tuple[str, int]:
        return "192.168.1.102", 2369
