import textwrap

def main() -> None:
    text = (
        "Python is amazing. It has a huge standard library that saves you time "
        "and helps you write clean, maintainable code."
    )

    wrapped = textwrap.fill(text, width=40)
    print("Wrapped text:")
    print(wrapped)

    indented = textwrap.indent(wrapped, prefix="> ")
    print("\nIndented text:")
    print(indented)

    shortened = textwrap.shorten(text, width=50, placeholder="...")
    print("\nShortened text:")
    print(shortened)

if __name__ == "__main__":
    main()