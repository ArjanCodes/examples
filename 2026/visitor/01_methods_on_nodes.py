from dataclasses import dataclass
from html import escape


@dataclass(frozen=True)
class Paragraph:
    text: str

    def to_html(self) -> str:
        return f"<p>{escape(self.text)}</p>"

    def accessibility_issues(self) -> list[str]:
        return []

    def collect_assets(self) -> set[str]:
        return set()


@dataclass(frozen=True)
class Image:
    url: str
    alt_text: str

    def to_html(self) -> str:
        return f'<img src="{escape(self.url)}" alt="{escape(self.alt_text)}">'

    def accessibility_issues(self) -> list[str]:
        if self.alt_text:
            return []
        return [f"Image {self.url!r} has no alternative text"]

    def collect_assets(self) -> set[str]:
        return {self.url}


@dataclass(frozen=True)
class Section:
    title: str
    children: list[DocumentNode]

    def to_html(self) -> str:
        body = "\n".join(child.to_html() for child in self.children)
        return f"<section><h2>{escape(self.title)}</h2>\n{body}\n</section>"

    def accessibility_issues(self) -> list[str]:
        return [
            issue for child in self.children for issue in child.accessibility_issues()
        ]

    def collect_assets(self) -> set[str]:
        return set().union(*(child.collect_assets() for child in self.children))


type DocumentNode = Paragraph | Image | Section


def build_document() -> DocumentNode:
    return Section(
        title="Visitor patterns",
        children=[
            Paragraph("Document nodes also know every operation performed on them."),
            Image(url="diagram.svg", alt_text=""),
        ],
    )


def main() -> None:
    document = build_document()
    print(document.to_html())
    print("Accessibility:", document.accessibility_issues())
    print("Assets:", document.collect_assets())


if __name__ == "__main__":
    main()
