from dataclasses import dataclass
from typing import Literal

SortOrder = Literal["relevance", "upload_date", "views"]
Duration = Literal["short", "medium", "long"]


@dataclass(frozen=True)
class Video:
    title: str
    duration_seconds: int
    is_short: bool
    region: str
    views: int


@dataclass(frozen=True)
class VideoSearchQuery:
    query: str
    category: str | None = None
    sort_by: SortOrder = "relevance"
    upload_date: str | None = None
    duration: Duration | None = None
    region: str = "US"
    include_shorts: bool = True
    max_results: int = 20
    language: str | None = None

    def __post_init__(self) -> None:
        if not self.query.strip():
            raise ValueError("Search query cannot be empty")

        if not 1 <= self.max_results <= 50:
            raise ValueError("max_results must be between 1 and 50")


def search_videos(search: VideoSearchQuery) -> list[Video]:
    validate_search(search)

    cache_key = get_cache_key(search)
    if cached_results := get_cached_results(cache_key):
        return cached_results

    backend_query = build_search_query(search)
    results = execute_search(backend_query)

    track_search(search)

    results = filter_by_duration(results, search.duration)
    results = exclude_shorts(results, search.include_shorts)
    results = limit_results(results, search.max_results)

    return results


def validate_search(search: VideoSearchQuery) -> None:
    print(f"Validating search: {search.query!r}")


def get_cache_key(search: VideoSearchQuery) -> str:
    return (
        f"{search.query}:"
        f"{search.category}:"
        f"{search.sort_by}:"
        f"{search.upload_date}:"
        f"{search.duration}:"
        f"{search.region}:"
        f"{search.include_shorts}:"
        f"{search.language}"
    )


def get_cached_results(cache_key: str) -> list[Video] | None:
    print(f"Checking cache for: {cache_key}")
    return None


def build_search_query(search: VideoSearchQuery) -> dict[str, object]:
    return {
        "text": search.query,
        "category": search.category,
        "sort": search.sort_by,
        "upload_date": search.upload_date,
        "duration": search.duration,
        "region": normalize_region(search.region),
        "include_shorts": search.include_shorts,
        "limit": search.max_results,
        "language": search.language,
    }


def normalize_region(region: str) -> str:
    return region.upper()


def execute_search(query: dict[str, object]) -> list[Video]:
    print(f"Executing backend query: {query}")

    return [
        Video("Python dependency injection explained", 900, False, "NL", 100_000),
        Video("Dependency injection in 60 seconds", 58, True, "NL", 250_000),
        Video("Clean architecture in Python", 1_800, False, "US", 80_000),
        Video("Python decorators explained", 480, False, "NL", 120_000),
    ]


def track_search(search: VideoSearchQuery) -> None:
    print(
        "Tracking search:",
        {
            "query": search.query,
            "category": search.category,
            "region": search.region,
            "include_shorts": search.include_shorts,
        },
    )


def filter_by_duration(
    videos: list[Video],
    duration: Duration | None,
) -> list[Video]:
    if duration == "long":
        return [video for video in videos if video.duration_seconds > 1_200]

    return videos


def exclude_shorts(
    videos: list[Video],
    include_shorts: bool,
) -> list[Video]:
    return [video for video in videos if include_shorts or not video.is_short]


def limit_results(
    videos: list[Video],
    max_results: int,
) -> list[Video]:
    return videos[:max_results]


def main() -> None:
    search = VideoSearchQuery(
        query="dependency injection",
        duration="long",
        region="NL",
        include_shorts=False,
        max_results=10,
        language="en",
    )

    videos = search_videos(search)

    for video in videos:
        print(f"- {video.title}")


if __name__ == "__main__":
    main()
