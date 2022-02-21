def main():
    # create a set of numbers
    my_set = {i * i for i in range(10)}
    print(my_set)

    # create a dictionary of numbers
    my_dict = {i: i * i for i in range(10)}
    print(my_dict)


if __name__ == "__main__":
    main()
