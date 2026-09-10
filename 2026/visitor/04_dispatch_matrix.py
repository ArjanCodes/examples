from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from html import escape
from typing import Literal


class Node:
    """A base class gives the dispatcher an inheritance hierarchy to search."""


@dataclass(frozen=True)
class Paragraph(Node):
    text: str


@dataclass(frozen=True)
class Image(Node):
    url: str
    alt_text: str


@dataclass(frozen=True)
class DecorativeImage(Image):
    """Uses Image handlers through inheritance-aware dispatch."""


@dataclass(frozen=True)
class Section(Node):
    title: str
    children: list[DocumentNode]


type DocumentNode = Paragraph | Image | Section
type Operation = Literal["html", "accessibility", "assets"]
type Result = str | list[str] | set[str]
type Handler = Callable[[Node], Result]


def html_paragraph(node: Node) -> Result:
    paragraph = node if isinstance(node, Paragraph) else None
    assert paragraph is not None
    return f"<p>{escape(paragraph.text)}</p>"


def html_image(node: Node) -> Result:
    image = node if isinstance(node, Image) else None
    assert image is not None
    return f'<img src="{escape(image.url)}" alt="{escape(image.alt_text)}">'


def html_section(node: Node) -> Result:
    section = node if isinstance(node, Section) else None
    assert section is not None
    body = "\n".join(apply(child, "html") for child in section.children)
    return f"<section><h2>{escape(section.title)}</h2>\n{body}\n</section>"


def image_accessibility(node: Node) -> Result:
    image = node if isinstance(node, Image) else None
    assert image is not None
    return [] if image.alt_text else [f"Image {image.url!r} has no alternative text"]


def section_accessibility(node: Node) -> Result:
    section = node if isinstance(node, Section) else None
    assert section is not None
    return [
        issue for child in section.children for issue in apply(child, "accessibility")
    ]


def collect_image_asset(node: Node) -> Result:
    image = node if isinstance(node, Image) else None
    assert image is not None
    return {image.url}


def collect_section_assets(node: Node) -> Result:
    section = node if isinstance(node, Section) else None
    assert section is not None
    return set().union(*(apply(child, "assets") for child in section.children))


def no_accessibility_issues(node: Node) -> Result:
    return []


def no_assets(node: Node) -> Result:
    return set()


HANDLERS: dict[tuple[type[Node], Operation], Handler] = {
    (Paragraph, "html"): html_paragraph,
    (Image, "html"): html_image,
    (Section, "html"): html_section,
    (Image, "accessibility"): image_accessibility,
    (Section, "accessibility"): section_accessibility,
    (Image, "assets"): collect_image_asset,
    (Section, "assets"): collect_section_assets,
}
DEFAULTS: dict[Operation, Handler] = {
    "accessibility": no_accessibility_issues,
    "assets": no_assets,
}


def find_handler(node: Node, operation: Operation) -> Handler:
    for node_type in type(node).__mro__:
        handler = HANDLERS.get((node_type, operation))
        if handler is not None:
            return handler
    try:
        return DEFAULTS[operation]
    except KeyError:
        message = f"No {operation!r} handler for {type(node).__name__}"
        raise ValueError(message) from None


def apply(node: Node, operation: Operation) -> Result:
    return find_handler(node, operation)(node)


def build_document() -> DocumentNode:
    return Section(
        title="Dispatch matrix",
        children=[
            Paragraph(
                "The registry flattens behavior into (type, operation) coordinates."
            ),
            DecorativeImage("diagram.svg", ""),
        ],
    )


def main() -> None:
    document = build_document()
    print(apply(document, "html"))
    print("Accessibility:", apply(document, "accessibility"))
    print("Assets:", apply(document, "assets"))


if __name__ == "__main__":
    main()
