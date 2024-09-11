from datetime import timedelta
import re
from typing import Tuple
from bragir.tracing.logger import logger

from bragir.srt.srt_part import SRTPart


def to_timestamp(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    milliseconds = td.microseconds // 1000

    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def to_timedelta(timestamp: str) -> timedelta:
    parts = re.split("[:,.]", timestamp)
    parts = [float(part) for part in parts]

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
