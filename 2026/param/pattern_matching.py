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

    @property
    def cache_key(self) -> str:
        return (
            f"{self.query}:"
            f"{self.category}:"
            f"{self.sort_by}:"
            f"{self.upload_date}:"
            f"{self.duration}:"
            f"{self.region}:"
            f"{self.include_shorts}:"
            f"{self.language}"
        )


def search_videos(search: VideoSearchQuery) -> list[Video]:

    if cached_results := get_cached_results(search.cache_key):
        return cached_results

    backend_query = build_search_query(search)
    results = execute_search(backend_query)

    track_search(search)

    results = filter_by_duration(results, search.duration)
    results = exclude_shorts(results, search.include_shorts)
    results = limit_results(results, search.max_results)

    return results


def get_cached_results(cache_key: str) -> list[Video] | None:
    print(f"Checking cache for: {cache_key}")
    return None


def build_search_query(search: VideoSearchQuery) -> dict[str, object]:

    # Example of structural pattern matching / object deconstruction
    match search:
        case VideoSearchQuery(sort_by="views", max_results=max_results):
            print(f"Building trending query with limit {max_results}")

        case VideoSearchQuery(sort_by="upload_date"):
            print("Building recent uploads query")

        case _:
            print("Building default relevance query")

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

    # Example of deconstructing the parameter object
    match search:
        case VideoSearchQuery(
            query=query,
            region="NL",
            include_shorts=False,
        ):
            print(f"Tracking Dutch long-form search: {query}")

        case VideoSearchQuery(query=query):
            print(f"Tracking generic search: {query}")


def filter_by_duration(
    videos: list[Video],
    duration: Duration | None,
) -> list[Video]:

    if duration == "short":
        return [video for video in videos if video.duration_seconds < 240]

    if duration == "medium":
        return [video for video in videos if 240 <= video.duration_seconds <= 1_200]

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

    print()

    for video in videos:
        print(f"- {video.title}")


if __name__ == "__main__":
    main()
