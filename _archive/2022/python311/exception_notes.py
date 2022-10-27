def main() -> None:
    try:
        raise TypeError("bad type")
    except TypeError as type_error:
        type_error.add_note("Add some information")
        raise


if __name__ == "__main__":
    main()
