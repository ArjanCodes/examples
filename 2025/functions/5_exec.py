def main() -> None:
    exec("def add(x, y): return x + y")

    print(add(3, 4))  # 7


if __name__ == "__main__":
    main()
