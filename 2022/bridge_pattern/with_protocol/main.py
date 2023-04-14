import logging

from stream.dslr_camera import DSLRCamera
from stream.twitch_stream import TwitchStreamingService
from stream.webcam import Webcam
from stream.youtube_stream import YouTubeStreamingService


def main() -> None:
    # setup logging
    logging.basicConfig(level=logging.INFO)

    # create a device and a streaming service
    device = Webcam()
    service = YouTubeStreamingService(device)

    # start streaming
    reference = service.start_stream()
    service.fill_buffer(reference)
    service.stop_stream(reference)

    # create another device and streaming service
    device2 = DSLRCamera()
    service2 = TwitchStreamingService(device2)

    # start streaming there as well
    reference2 = service2.start_stream()
    service2.fill_buffer(reference2)
    service2.stop_stream(reference2)


if __name__ == "__main__":
    main()
