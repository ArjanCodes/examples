def print_input(input: str | int) -> None:
    if isinstance(input, str):
        print("String:", input)
    else:
        print("Number:", input)
