from iot.service import IOTService
from message.helper import Message as Msg
from network.connection import Connection


def send_msg_to_speaker(service: IOTService, speaker_id: str, msg: str) -> None:
    # create a connection to the smart speaker
    speaker_ip, speaker_port = service.get_device(speaker_id).connection_info()
    speaker_connection = Connection(speaker_ip, speaker_port)

    # construct a message
    message = Msg("SERVER", speaker_id, msg)

    # send the message
    speaker_connection.connect()
    speaker_connection.send(message.b64)
    speaker_connection.disconnect()
