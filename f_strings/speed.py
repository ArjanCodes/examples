import timeit
from string import Template


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


TEMPLATE = Template("$name is from $country.")


def template():
    name = "Arjan"
    country = "The Netherlands"
    _ = TEMPLATE.substitute(name=name, country=country)


def main() -> None:
    print(
        "perc_format:",
        timeit.timeit(
            perc_format,
            number=100000,
        ),
    )
    print(
        "str_format:",
        timeit.timeit(
            str_format,
            number=100000,
        ),
    )
    print(
        "template:",
        timeit.timeit(
            template,
            number=100000,
        ),
    )

    print(
        "f-string:",
        timeit.timeit(
            f_string,
            number=100000,
        ),
    )


if __name__ == "__main__":
    main()
