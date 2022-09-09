from datetime import datetime

from pytz import timezone


def main() -> None:
    some_date = datetime(2022, 10, 9, 18, 0, 0)
    # Create timezone UTC
    utc = timezone("UTC")
    # Localize date & time
    loc = utc.localize(some_date)
    print(loc)

    # Convert localized date & time into the Australia/Sydney timezone
    sydney = timezone("Australia/Sydney")
    print(loc.astimezone(sydney))

    # Convert localized date & time into Europe/Amsterdam timezone
    amsterdam = timezone("Europe/Amsterdam")
    print(loc.astimezone(amsterdam))


if __name__ == "__main__":
    main()
