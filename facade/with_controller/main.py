from functools import partial

from gui import SmartApp
from iot.devices import SmartSpeakerDevice
from iot.service import IOTService
from speaker_controller import send_msg_to_speaker


def main():
    # create a IOT service
    service = IOTService()

    # create the smart speaker
    smart_speaker = SmartSpeakerDevice()
    speaker_id = service.register_device(smart_speaker)
    toggle_speaker_fn = partial(
        send_msg_to_speaker, service=service, speaker_id=speaker_id
    )

    app = SmartApp(toggle_speaker_fn)
    app.mainloop()


if __name__ == "__main__":
    main()
