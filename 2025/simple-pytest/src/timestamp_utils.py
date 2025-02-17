import re
from datetime import timedelta
from typing import Tuple

from src.srt.srt_part import SRTPart
from src.tracing.logger import logger


def to_timestamp(td: timedelta) -> str:
    # if td is negative return 0 timestamp
    if td.total_seconds() < 0:
        return "00:00:00.000"

    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    milliseconds = td.microseconds // 1000

    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def to_timedelta(timestamp: str) -> timedelta:
    splitted_timestamps = re.split("[:,.]", timestamp)
    parts = [float(main_part) for main_part in splitted_timestamps]

    if len(parts) == 3:
        return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])

    return timedelta(
        hours=parts[0], minutes=parts[1], seconds=parts[2], milliseconds=parts[3]
    )


def update_timestamps(videos_srts: list[Tuple[int, list[SRTPart]]]) -> list[SRTPart]:
    index_pointer = 1
    video_end_time = timedelta(hours=0, minutes=0, seconds=0)
    all_srt_parts: list[SRTPart] = []

    logger.info("Updating timestamps")
    for _order, srt_parts in sorted(videos_srts):
        for srt_part in srt_parts:
            srt_part.start_time = to_timestamp(
                to_timedelta(srt_part.start_time) + video_end_time
            )
            srt_part.end_time = to_timestamp(
                to_timedelta(srt_part.end_time) + video_end_time
            )
            srt_part.index = index_pointer
            index_pointer += 1
            all_srt_parts.append(srt_part)
        video_end_time = to_timedelta(srt_parts[-1].end_time)

    return all_srt_parts
