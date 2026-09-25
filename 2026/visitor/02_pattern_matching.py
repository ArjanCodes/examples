from __future__ import annotations

from dataclasses import dataclass
from html import escape


@dataclass(frozen=True)
class Paragraph:
    text: str


@dataclass(frozen=True)
class Image:
    url: str
    alt_text: str


@dataclass(frozen=True)
class Section:
    title: str
    children: list[DocumentNode]


type DocumentNode = Paragraph | Image | Section


def render_html(node: DocumentNode) -> str:
    match node:
        case Paragraph(text):
            return f"<p>{escape(text)}</p>"
        case Image(url, alt_text):
            return f'<img src="{escape(url)}" alt="{escape(alt_text)}">'
        case Section(title, children):
            body = "\n".join(render_html(child) for child in children)
            return f"<section><h2>{escape(title)}</h2>\n{body}\n</section>"


def accessibility_issues(node: DocumentNode) -> list[str]:
    match node:
        case Paragraph():
            return []
        case Image(url, alt_text=""):
            return [f"Image {url!r} has no alternative text"]
        case Image():
            return []
        case Section(children=children):
            return [
                issue for child in children for issue in accessibility_issues(child)
            ]


def collect_assets(node: DocumentNode) -> set[str]:
    match node:
        case Paragraph():
            return set()
        case Image(url):
            return {url}
        case Section(children=children):
            return set().union(*(collect_assets(child) for child in children))


def build_document() -> DocumentNode:
    return Section(
        title="Pattern matching",
        children=[
            Paragraph("Operations are now grouped by what they do."),
            Image("diagram.svg", ""),
        ],
    )


def main() -> None:
    document = build_document()
    print(render_html(document))
    print("Accessibility:", accessibility_issues(document))
    print("Assets:", collect_assets(document))


if __name__ == "__main__":
    main()
