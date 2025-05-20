from typing import Any

from youtube_search import YoutubeSearch


def search_youtube(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    """Search YouTube for a given query and return the results."""
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    return results


def construct_video_url(video_id: str) -> str:
    """Construct a YouTube video URL from the video ID."""
    return f"https://www.youtube.com/watch?v={video_id}"
