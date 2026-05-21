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


def search_videos(
    query: str,
    category: str | None = None,
    sort_by: SortOrder = "relevance",
    upload_date: str | None = None,
    duration: Duration | None = None,
    region: str = "US",
    include_shorts: bool = True,
    max_results: int = 20,
    language: str | None = None,
) -> list[Video]:
    validate_search(
        query=query,
        category=category,
        sort_by=sort_by,
        upload_date=upload_date,
        duration=duration,
        region=region,
        include_shorts=include_shorts,
        max_results=max_results,
    )

    cache_key = get_cache_key(
        query=query,
        category=category,
        sort_by=sort_by,
        upload_date=upload_date,
        duration=duration,
        region=region,
        include_shorts=include_shorts,
        language=language,
    )

    if cached_results := get_cached_results(cache_key):
        return cached_results

    backend_query = build_search_query(
        query=query,
        category=category,
        sort_by=sort_by,
        upload_date=upload_date,
        duration=duration,
        region=region,
        include_shorts=include_shorts,
        max_results=max_results,
        language=language,
    )

    results = execute_search(backend_query)

    track_search(
        query=query,
        category=category,
        region=region,
        include_shorts=include_shorts,
    )

    results = filter_by_duration(results, duration)
    results = exclude_shorts(results, include_shorts)
    results = limit_results(results, max_results)

    return results


def validate_search(
    query: str,
    category: str | None,
    sort_by: SortOrder,
    upload_date: str | None,
    duration: Duration | None,
    region: str,
    include_shorts: bool,
    max_results: int,
) -> None:
    if not query.strip():
        raise ValueError("Search query cannot be empty")

    if not 1 <= max_results <= 50:
        raise ValueError("max_results must be between 1 and 50")


def get_cache_key(
    query: str,
    category: str | None,
    sort_by: SortOrder,
    upload_date: str | None,
    duration: Duration | None,
    region: str,
    include_shorts: bool,
    language: str | None,
) -> str:
    return (
        f"{query}:"
        f"{category}:"
        f"{sort_by}:"
        f"{upload_date}:"
        f"{duration}:"
        f"{region}:"
        f"{include_shorts}:"
        f"{language}"
    )


def get_cached_results(cache_key: str) -> list[Video] | None:
    print(f"Checking cache for: {cache_key}")
    return None


def build_search_query(
    query: str,
    category: str | None,
    sort_by: SortOrder,
    upload_date: str | None,
    duration: Duration | None,
    region: str,
    include_shorts: bool,
    max_results: int,
    language: str | None,
) -> dict[str, object]:
    return {
        "text": query,
        "category": category,
        "sort": sort_by,
        "upload_date": upload_date,
        "duration": duration,
        "region": normalize_region(region),
        "include_shorts": include_shorts,
        "limit": max_results,
        "language": language,
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


def track_search(
    query: str,
    category: str | None,
    region: str,
    include_shorts: bool,
) -> None:
    print(
        "Tracking search:",
        {
            "query": query,
            "category": category,
            "region": region,
            "include_shorts": include_shorts,
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
    videos = search_videos(
        query="python dependency injection",
        duration="long",
        region="NL",
        include_shorts=False,
        max_results=10,
        language="en",
    )

    for video in videos:
        print(f"- {video.title}")


if __name__ == "__main__":
    main()
