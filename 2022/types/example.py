def luhn_checksum_with_doc(number):
    """
    Check that the provided number passes the Luhn checksum algorithm.
    For more information, see: https://en.wikipedia.org/wiki/Luhn_algorithm.

            Parameters:
                    number (str): A number represented as a string.

            Returns:
                    luhn_checksum (bool): True if the Luhn checksum is correct, False otherwise.
    """

    def digits_of(nr):
        return [int(d) for d in nr]

    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for digit in even_digits:
        checksum += sum(digits_of(str(digit * 2)))
    return checksum % 10 == 0


def luhn_checksum_with_type_hints(number: str) -> bool:
    def digits_of(nr: str) -> list[int]:
        return [int(d) for d in nr]

    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for digit in even_digits:
        checksum += sum(digits_of(str(digit * 2)))
    return checksum % 10 == 0


def luhn_checksum(number):
    def digits_of(nr):
        return [int(d) for d in nr]

    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for digit in even_digits:
        checksum += sum(digits_of(str(digit * 2)))
    return checksum % 10 == 0


def main():
    print(luhn_checksum(1249190007575069))  # oops
    print(luhn_checksum_with_doc(1249190007575069))  # oops

    print(luhn_checksum_with_type_hints("1249190007575069"))


if __name__ == "__main__":
    main()
