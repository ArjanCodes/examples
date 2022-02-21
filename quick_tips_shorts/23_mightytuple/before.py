import random


# return a tuple as a result of a function
def random_point() -> tuple[int, int]:
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    return x, y


def main():
    var1 = 3
    var2 = 4

    # swap values
    tmp = var1
    var1 = var2
    var2 = tmp
    print(var1, var2)

    # unpack a list
    my_list: list[int] = [1, 2, 3]
    var1 = my_list[0]
    var2 = my_list[1]
    var3 = my_list[2]
    print(var1, var2, var3)

    x, y = random_point()
    print(x, y)


if __name__ == "__main__":
    main()
