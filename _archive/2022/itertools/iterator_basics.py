def main() -> None:

    countries = ("Germany", "France", "Italy", "Spain", "Portugal", "Greece")
    country_iterator = iter(countries)

    print(next(country_iterator))
    print(next(country_iterator))
    print(next(country_iterator))
    print(next(country_iterator))
    print(next(country_iterator))
    print(next(country_iterator))
    # print(next(my_iterator))  # this raises a StopIteration exception

    # alternatively, we can use a for loop
    for country in countries:
        print(country)

    # a for loop creates an iterator object and executes the next() method for each iteration
    # behind the scenes, the for loop is equivalent to the following code:
    country_iterator = iter(countries)
    while True:
        try:
            country = next(country_iterator)
        except StopIteration:
            break
        else:
            print(country)

    # you can also call iter with a sentinel value
    # this is useful when you want to iterate over a stream of data
    # for example, you can read a file line by line
    # the sentinel value is a value that indicates the end of the stream
    # in this case, the sentinel value is an empty string
    with open("countries.txt") as f:
        for line in iter(f.readline, ""):
            print(line, end="")


if __name__ == "__main__":
    main()
