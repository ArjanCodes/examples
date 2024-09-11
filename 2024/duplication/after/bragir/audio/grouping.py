from pydub import AudioSegment

from bragir.tracing.logger import logger


def combine(audio_segments: list[AudioSegment]) -> AudioSegment | None:
    if len(audio_segments) >= 1:
        combined_no_crossfade = audio_segments[0]
        for segment in audio_segments[1:]:
            combined_no_crossfade += segment
        return combined_no_crossfade

    return None


def group_audio_segments(
    audio_segments: list[AudioSegment], duration_limit_seconds: float
) -> list[AudioSegment]:
    logger.info(f"Grouping {len(audio_segments)} audio segments")

    if not audio_segments:
        return []

    total_duration = sum(obj.duration_seconds for obj in audio_segments)
    if total_duration < duration_limit_seconds:
        return [combine(audio_segments)]

    grouped_audio_segments = []
    current_group = []
    total_duration = 0.0

    for obj in audio_segments:
        if total_duration + obj.duration_seconds > duration_limit_seconds:
            combined = combine(current_group)
            if combined:  # Ensuring that None is not appended
                grouped_audio_segments.append(combined)
            current_group = []
            total_duration = 0.0

        current_group.append(obj)
        total_duration += obj.duration_seconds

    # Handle the last group if not empty
    combined = combine(current_group)
    if combined:
        grouped_audio_segments.append(combined)

    logger.info(f"Grouped into {len(grouped_audio_segments)} audio segments")

    return grouped_audio_segments
