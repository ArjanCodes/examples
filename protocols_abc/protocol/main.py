from iot.devices import CurtainsDevice, HueLightDevice, SmartSpeakerDevice
from iot.diagnostics import collect_diagnostics
from iot.message import Message, MessageType
from iot.service import IOTService


class TestingDevice:
    def status_update(self) -> str:
        return "test_status_ok"


def main() -> None:
    # create a IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    curtains = CurtainsDevice()
    hue_light_id = service.register_device(hue_light)
    speaker_id = service.register_device(speaker)
    curtains_id = service.register_device(curtains)

    # create a few programs
    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.PLAY_SONG, "Miles Davis - Kind of Blue"),
        Message(curtains_id, MessageType.OPEN),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(curtains_id, MessageType.CLOSE),
    ]

    # run the programs
    service.run_program(wake_up_program)
    service.run_program(sleep_program)

    # collect some diagnostics
    testing_device = TestingDevice()
    collect_diagnostics(testing_device)


if __name__ == "__main__":
    main()
