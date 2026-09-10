from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Protocol


class DocumentVisitor[T](Protocol):
    def visit_paragraph(self, node: Paragraph) -> T: ...

    def visit_image(self, node: Image) -> T: ...

    def visit_section(self, node: Section) -> T: ...


@dataclass(frozen=True)
class Paragraph:
    text: str

    def accept[T](self, visitor: DocumentVisitor[T]) -> T:
        return visitor.visit_paragraph(self)


@dataclass(frozen=True)
class Image:
    url: str
    alt_text: str

    def accept[T](self, visitor: DocumentVisitor[T]) -> T:
        return visitor.visit_image(self)


@dataclass(frozen=True)
class Section:
    title: str
    children: list[DocumentNode]

    def accept[T](self, visitor: DocumentVisitor[T]) -> T:
        return visitor.visit_section(self)


type DocumentNode = Paragraph | Image | Section


class HtmlRenderer(DocumentVisitor[str]):
    def visit_paragraph(self, node: Paragraph) -> str:
        return f"<p>{escape(node.text)}</p>"

    def visit_image(self, node: Image) -> str:
        return f'<img src="{escape(node.url)}" alt="{escape(node.alt_text)}">'

    def visit_section(self, node: Section) -> str:
        body = "\n".join(child.accept(self) for child in node.children)
        return f"<section><h2>{escape(node.title)}</h2>\n{body}\n</section>"


class AccessibilityChecker(DocumentVisitor[list[str]]):
    def visit_paragraph(self, node: Paragraph) -> list[str]:
        return []

    def visit_image(self, node: Image) -> list[str]:
        return [] if node.alt_text else [f"Image {node.url!r} has no alternative text"]

    def visit_section(self, node: Section) -> list[str]:
        return [issue for child in node.children for issue in child.accept(self)]


def build_document() -> DocumentNode:
    return Section(
        title="Classic Visitor",
        children=[
            Paragraph("Adding visitors is easy once node types are stable."),
            Image("diagram.svg", ""),
        ],
    )


def main() -> None:
    document = build_document()
    print(document.accept(HtmlRenderer()))
    print("Accessibility:", document.accept(AccessibilityChecker()))


if __name__ == "__main__":
    main()
