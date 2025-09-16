import httpx
from bs4 import BeautifulSoup

NEWS_URL = "https://news.ycombinator.com"

def fetch_headlines(limit: int = 5) -> list[str]:
    response = httpx.get(NEWS_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    titles = [a.get_text() for a in soup.select(".titleline a")]
    return titles[:limit]
