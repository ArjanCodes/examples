from dataclasses import dataclass
from typing import Protocol


class DocumentState(Protocol):
    def edit(self):
        ...

    def review(self):
        ...

    def finalize(self):
        ...


class DocumentContext(Protocol):
    content: list[str]

    def set_state(self, state: DocumentState) -> None:
        ...

    def edit(self):
        ...

    def review(self):
        ...

    def finalize(self):
        ...

    def show_content(self):
        ...


@dataclass
class Draft:
    document: DocumentContext

    def edit(self):
        print("Editing the document...")
        self.document.content.append("Edited content.")

    def review(self):
        print("The document is now under review.")
        self.document.set_state(Reviewed(self.document))

    def finalize(self):
        print("You need to review the document before finalizing.")


@dataclass
class Reviewed:
    document: DocumentContext

    def edit(self):
        print("The document is under review, cannot edit now.")

    def review(self):
        print("The document is already reviewed.")

    def finalize(self):
        print("Finalizing the document...")
        self.document.set_state(Finalized(self.document))


@dataclass
class Finalized:
    document: DocumentContext

    def edit(self):
        print("The document is finalized. Editing is not allowed.")

    def review(self):
        print("The document is finalized. Review is not possible.")

    def finalize(self):
        print("The document is already finalized.")


class Document:
    def __init__(self):
        self.state: DocumentState = Draft(self)
        self.content: list[str] = []

    def set_state(self, state: DocumentState):
        self.state = state

    def edit(self):
        self.state.edit()

    def review(self):
        self.state.review()

    def finalize(self):
        self.state.finalize()

    def show_content(self):
        print("Document content:", " ".join(self.content))


def main() -> None:
    document = Document()

    document.edit()  # Expected: "Editing the document..."
    document.show_content()  # Expected: "Document content: Edited content."
    document.finalize()  # Expected: "You need to review the document before finalizing."
    document.review()  # Expected: "The document is now under review."
    document.edit()  # Expected: "The document is under review, cannot edit now."
    document.finalize()  # Expected: "Finalizing the document..."
    document.edit()  # Expected: "The document is finalized. Editing is not allowed."


if __name__ == "__main__":
    main()
