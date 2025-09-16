import typer
from rich.console import Console
from core.news import fetch_headlines
from summarizer.summarize import summarize_text
import os


from dotenv import load_dotenv

load_dotenv()  # Load OPENAI_API_KEY from .env

app = typer.Typer()
console = Console()

@app.command()
def headlines(limit: int = 5):
    headlines = fetch_headlines(limit)
    console.print(f"[bold blue]Top {limit} headlines from Hacker News:[/bold blue]")
    for i, title in enumerate(headlines, 1):
        console.print(f"[green]{i}.[/green] {title}")

    api_key = os.environ.get("OPENAI_API_KEY")

    console.print("\n[bold blue]Summary:[/bold blue]")
    summary = summarize_text("\n".join(headlines), api_key)
    console.print(summary)

if __name__ == "__main__":
    app()
