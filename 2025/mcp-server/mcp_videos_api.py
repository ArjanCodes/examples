from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("videos")

API_URL = "http://localhost:8000/videos"  # Adjust if hosted elsewhere


def format_video(video: dict[str, Any]) -> str:
    """Format a video feature into a readable string."""
    return f"""
        Title: {video.get("title", "Unknown")}
        Channel: {video.get("channel", "Unknown")}
        Duration: {video.get("duration", "Unknown")}
        Description: {video.get("description", "No description available")}
        Views: {video.get("views", "Unknown")}
        URL: {video.get("url", "Unknown")}
        Published: {video.get("publish_time", "Unknown")}
       """


@mcp.tool()
async def get_videos(search: str, max_results: int) -> str:
    """Get videos for a search query via external FastAPI endpoint.

    Args:
        search: Search query string
        max_results: Maximum number of results to return
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                API_URL, params={"search": search, "max_results": max_results}
            )
            response.raise_for_status()
            data = response.json()
            videos = data.get("results", [])
        except Exception as e:
            return f"Error retrieving videos: {str(e)}"

    if not videos:
        return "No videos found."

    return "\n---\n".join(format_video(video) for video in videos)


if __name__ == "__main__":
    mcp.run(transport="stdio")
