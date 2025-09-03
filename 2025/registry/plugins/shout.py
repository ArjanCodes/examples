from registry import register_command
from rich import print


@register_command("text", "shout")
def shout(text: str) -> None:
    print(f"[bold red]{text.upper()}!!![/bold red]")
