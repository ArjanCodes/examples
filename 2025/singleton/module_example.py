import config

def main() -> None:
    if config.debug:
        print(config.db_uri)

if __name__ == "__main__":
    main()