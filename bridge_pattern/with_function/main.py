import logging

from stream.dslr_camera import get_dslr_buffer_data
from stream.twitch_stream import TwitchStreamingService
from stream.webcam import get_webcam_buffer_data
from stream.youtube_stream import YouTubeStreamingService


def main():
    # setup logging
    logging.basicConfig(level=logging.INFO)

    # create a device and a streaming service
    service = YouTubeStreamingService(get_webcam_buffer_data)

    # start streaming
    reference = service.start_stream()
    service.fill_buffer(reference)
    service.stop_stream(reference)

    # create another device and streaming service
    service2 = TwitchStreamingService(get_dslr_buffer_data)

    # start streaming there as well
    reference2 = service2.start_stream()
    service2.fill_buffer(reference2)
    service2.stop_stream(reference2)


if __name__ == "__main__":
    main()
