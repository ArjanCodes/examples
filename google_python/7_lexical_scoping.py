def my_function():
    x: int = 3

    def internal_function():
        print(x)
        # x = 5 (this turns x into a variable local to internal_function, leading to an error)

    # if you replace this by 'for x in range(3):' it will now print 0, 1, 2 because x has become
    # a variable local to my_function
    for _ in range(3):
        internal_function()


def main():
    my_function()


if __name__ == "__main__":
    main()
