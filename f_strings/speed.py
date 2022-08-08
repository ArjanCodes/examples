import timeit


def perc_format():
    name = "Arjan"
    country = "The Netherlands"
    _ = "%s is from %s." % (name, country)


def str_format():
    name = "Arjan"
    country = "The Netherlands"
    _ = "{} is from {}.".format(name, country)


def f_string():
    name = "Arjan"
    country = "The Netherlands"
    _ = f"{name} is from {country}."


def main() -> None:
    print(
        timeit.timeit(
            perc_format,
            number=100000,
        )
    )
    print(
        timeit.timeit(
            str_format,
            number=100000,
        )
    )
    print(
        timeit.timeit(
            f_string,
            number=100000,
        )
    )


if __name__ == "__main__":
    main()
