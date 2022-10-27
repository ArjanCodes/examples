import pendulum


def main() -> None:

    # Pendulum dates are timezone aware by default
    some_date = pendulum.datetime(2022, 10, 9, 18, 0, tz="UTC")
    print(some_date)

    # Convert date & time into the Australia/Sydney timezone
    print(some_date.in_timezone("Australia/Sydney"))

    # Convert date & time into Europe/Amsterdam timezone
    print(some_date.in_timezone("Europe/Amsterdam"))

    # Pendulum handles time transitions properly
    dt = pendulum.datetime(2013, 3, 31, 1, 59, 59, 999999, tz="Europe/Paris")
    print(dt)
    dt = dt.add(microseconds=1)
    print(dt)
    dt = dt.subtract(microseconds=1)
    print(dt)

    # setting the locale
    pendulum.set_locale("nl")

    # print localized date
    print(some_date.format("dddd DD MMMM YYYY"))

    # you can override the locale in the format method
    print(some_date.format("dddd DD MMMM YYYY", locale="it"))

    # localized formats
    print(some_date.format("LT"))
    print(some_date.format("LLLL"))

    # print a humanized timespan
    print(pendulum.now().add(years=1).diff_for_humans())

    # also here you can override the locale
    print(pendulum.now().add(years=1).diff_for_humans(locale="de"))

    # you can also indicate that the string should be absolute
    print(pendulum.now().add(years=1).diff_for_humans(absolute=True))

    # extra properties
    print(pendulum.now().day_of_year)
    print(pendulum.now().day_of_week)
    print(pendulum.now().week_of_month)
    print(pendulum.now().week_of_year)
    print(pendulum.now().days_in_month)
    print(pendulum.now().int_timestamp)
    print(pendulum.now().float_timestamp)

    # helpful methods
    print(pendulum.now().start_of("day"))
    print(pendulum.now().end_of("day"))

    # durations support years and months
    duration = pendulum.duration(years=3, months=3)
    print(duration.days)


if __name__ == "__main__":
    main()
