from dataclasses import dataclass
from functools import singledispatch
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


@singledispatch
def render_html(node: object) -> str:
    raise TypeError(f"Cannot render {type(node).__name__}")


@render_html.register
def _(node: Paragraph) -> str:
    return f"<p>{escape(node.text)}</p>"


@render_html.register
def _(node: Image) -> str:
    return f'<img src="{escape(node.url)}" alt="{escape(node.alt_text)}">'


@render_html.register
def _(node: Section) -> str:
    body = "\n".join(render_html(child) for child in node.children)
    return f"<section><h2>{escape(node.title)}</h2>\n{body}\n</section>"


@singledispatch
def accessibility_issues(node: object) -> list[str]:
    # The default serves types without special accessibility rules.
    return []


@accessibility_issues.register
def _(node: Image) -> list[str]:
    return [] if node.alt_text else [f"Image {node.url!r} has no alternative text"]


@accessibility_issues.register
def _(node: Section) -> list[str]:
    return [issue for child in node.children for issue in accessibility_issues(child)]


def build_document() -> DocumentNode:
    return Section(
        title="Single dispatch",
        children=[
            Paragraph("Nodes stay unaware of the operations."),
            Image("diagram.svg", ""),
        ],
    )


def main() -> None:
    document = build_document()
    print(render_html(document))
    print("Accessibility:", accessibility_issues(document))


if __name__ == "__main__":
    main()
