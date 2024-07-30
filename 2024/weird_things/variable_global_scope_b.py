def main() -> None:
    [x for x in range(7) if x == 6 and print(f"{x}: for x inside loop")]
    print(x, ": x in global")  # will return an error


if __name__ == "__main__":
    main()
