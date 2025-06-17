from dataclasses import dataclass
from typing import Self


@dataclass
class HTMLPage:
    title: str
    body_elements: list[str]

    def render(self) -> str:
        body = "\n".join(self.body_elements)
        return f"""<!DOCTYPE html>
                    <html>
                    <head><title>{self.title}</title></head>
                    <body>
                    {body}
                    </body>
                    </html>"""


class HTMLBuilder:
    def __init__(self) -> None:
        self._title: str = "Untitled"
        self._body: list[str] = []

    def set_title(self, title: str) -> Self:
        self._title = title
        return self

    def add_header(self, text: str, level: int = 1) -> Self:
        self._body.append(f"<h{level}>{text}</h{level}>")
        return self

    def add_paragraph(self, text: str) -> Self:
        self._body.append(f"<p>{text}</p>")
        return self

    def add_button(self, label: str, onclick: str = "#") -> Self:
        self._body.append(
            f"<button onclick=\"location.href='{onclick}'\">{label}</button>"
        )
        return self

    def build(self) -> HTMLPage:
        return HTMLPage(self._title, self._body)
