import tomllib


def main() -> None:
    # Load a TOML file
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    print(data["project"]["name"])


if __name__ == "__main__":
    main()
