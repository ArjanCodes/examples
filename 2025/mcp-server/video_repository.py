from typing import Any

from youtube_search import YoutubeSearch


def search_youtube(query: str, max_results: int = 10) -> dict[str, Any]:
    """Search YouTube for a given query and return the results."""
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    return results
