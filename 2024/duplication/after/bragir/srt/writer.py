from bragir.file import (
    chunk_content_into_srt_parts,
)
from bragir.time import update_timestamps

from .srt_part import SRTPart


def write_srt_to_file(transcripts: list[str], target_path: str) -> str:
    videos_srts: list[tuple[int, list[SRTPart]]] = [
        (order, chunk_content_into_srt_parts(transcript))
        for order, transcript in enumerate(transcripts)
    ]

    sorted_videos = sorted(videos_srts)

    srt_parts = update_timestamps(sorted_videos)

    contents = "".join([srt_part.srt_format for srt_part in srt_parts])

    with open(target_path, "w", encoding="utf-8") as fileIO:
        fileIO.write(contents)

    return target_path
