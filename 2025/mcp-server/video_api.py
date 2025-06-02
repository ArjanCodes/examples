from typing import Optional

import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel
from yt_helper import construct_video_url, search_youtube

app = FastAPI(title="YouTube Video Search API")


class Video(BaseModel):
    title: str
    channel: str
    duration: str
    description: Optional[str]
    views: Optional[str]
    url: str
    publish_time: Optional[str]


@app.get("/videos", response_model=list[Video])
async def get_videos(
    search: str = Query(..., description="Search query"),
    max_results: int = Query(
        5, ge=1, le=50, description="Max number of videos to return"
    ),
):
    """Search for YouTube videos."""
    results = search_youtube(search, max_results=max_results)

    formatted = [
        Video(
            title=video.get("title", "Unknown"),
            channel=video.get("channel", "Unknown"),
            duration=video.get("duration", "Unknown"),
            description=video.get("description", None),
            views=video.get("views", None),
            url=construct_video_url(video.get("id", "dQw4w9WgXcQ")),
            publish_time=video.get("publish_time", None),
        )
        for video in results
    ]

    return formatted


def main():
    uvicorn.run("video_api:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
