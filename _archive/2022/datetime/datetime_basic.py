import time
from datetime import datetime


def main() -> None:
    print(time.time())
    # simple dates
    some_date = datetime(2022, 10, 9, 18, 0, 0)
    print(some_date)

    # ISO 8601 parsing
    some_date = datetime.fromisoformat("2022-09-16T14:05:14")
    print(some_date)

    # get the present date
    today = datetime.now()
    print(today)

    # date comparison
    print(some_date < today)


if __name__ == "__main__":
    main()
