import textwrap


def main() -> None:
    text = "This is a sample text that will be wrapped to a specified width using the textwrap module in Python."
    print(textwrap.fill(text, width=40))

if __name__ == "__main__":
    main()