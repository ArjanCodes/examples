import time
from datetime import datetime


def main() -> None:
    print(time.time())
    # using ISO dates
    some_date = datetime(2022, 10, 9, 18, 0, 0)
    print(some_date)

    # get the present date
    today = datetime.now()
    print(today)


if __name__ == "__main__":
    main()
