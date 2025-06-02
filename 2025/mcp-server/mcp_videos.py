from typing import Any

from mcp.server.fastmcp import FastMCP
from yt_helper import construct_video_url, search_youtube

# Initialize FastMCP server
mcp = FastMCP("videos")


def format_video(video: dict[str, Any]) -> str:
    """Format a video feature into a readable string."""
    return f"""
        Title: {video.get("title", "Unknown")}
        Channel: {video.get("channel", "Unknown")}
        Duration: {video.get("duration", "Unknown")}
        Description: {video.get("description", "No description available")}
        Views: {video.get("views", "Unknown")}
        URL: {construct_video_url(video.get("id", "dQw4w9WgXcQ"))}
        Published: {video.get("publish_time", "Unknown")}
       """


@mcp.tool()
async def get_videos(search: str, max_results: int) -> str:
    """Get videos for a search query.

    Args:
        search: Search query string
        max_results: Maximum number of results to return
    """
    results = search_youtube(search, max_results=max_results)
    if not results:
        return "No videos found."

    videos = [format_video(video) for video in results]
    return "\n---\n".join(videos)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
