import logging

# from my_package.my_module import my_function <- not good!
from my_package import my_module


def main():
    logging.basicConfig(level=logging.INFO)

    my_module.my_function()


if __name__ == "__main__":
    main()
