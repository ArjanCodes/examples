from htmlbuilder import HTMLBuilder
from viewer import HTMLViewer


def main() -> None:
    # --- Build UI Page ---
    builder = HTMLBuilder()
    page = (
        builder.set_title("Builder Pattern UI")
        .add_header("Hello from Python!", level=1)
        .add_paragraph("This page was generated using the Builder Pattern.")
        .add_button("Visit ArjanCodes", onclick="https://arjan.codes")
        .build()
    )

    file_path = "page.html"
    with open(file_path, "w") as f:
        f.write(page.render())

    print("HTML page written to 'page.html'")

    # --- Start Viewer ---
    viewer = HTMLViewer(filename=file_path)
    viewer.start()


if __name__ == "__main__":
    main()
