def main() -> None:
    for x in range(7):
        if x == 6:
            print(x, ": for x inside loop")
    print(x, ": x in global/scope")


if __name__ == "__main__":
    main()
