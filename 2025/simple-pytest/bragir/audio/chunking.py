from pydub import AudioSegment  # type:ignore
from pydub.silence import split_on_silence  # type:ignore

from bragir.audio.grouping import group_audio_segments
from bragir.config import get_config
from bragir.constants import DURATION_SECONDS_25MB
from bragir.tracing.logger import logger


def chunk_audio(
    file_path: str,
    format: str = "mp4",
) -> list[AudioSegment]:
    config = get_config()

    if config is None:
        logger.error("Config not found")
        exit(1)

    audio_config = config.audio

    sound: AudioSegment = AudioSegment.from_file(  # type:ignore
        file=file_path
    )

    logger.info(f"Spliting {file_path} on silence")

    chunks: list[AudioSegment] = split_on_silence(
        sound,
        min_silence_len=audio_config.min_silence_len,
        silence_thresh=audio_config.silence_thresh,
        keep_silence=audio_config.keep_silence,
    )  # type: ignore

    logger.info(f"Number of chunks {len(chunks)} when splitted on silence")

    limit = DURATION_SECONDS_25MB[format] * 0.9

    logger.info(f"Limit {limit} seconds for {format}")

    audio_segments = group_audio_segments(chunks, limit)

    logger.info(f"Number of audio segments {len(audio_segments)}")

    return audio_segments
