from iot.devices import SmartSpeakerDevice
from iot.service import IOTService
from message.helper import Message as Msg
from network.connection import Connection

SERVICE = IOTService()


class Speaker:
    def __init__(self) -> None:
        # create the speaker device
        smart_speaker = SmartSpeakerDevice()
        self.speaker_id = SERVICE.register_device(smart_speaker)

    def send_message(self, msg: str) -> None:
        # create a connection to the smart speaker
        speaker_ip, speaker_port = SERVICE.get_device(self.speaker_id).connection_info()
        speaker_connection = Connection(speaker_ip, speaker_port)

        # construct a message
        message = Msg("SERVER", self.speaker_id, msg)

        # send the message
        speaker_connection.connect()
        speaker_connection.send(message.b64)
        speaker_connection.disconnect()
