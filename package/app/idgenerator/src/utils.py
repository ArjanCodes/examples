def digits_of(number_sequence: str) -> list[int]:
    return [int(digit) for digit in str(number_sequence)]


def luhn_checksum(card_number: str) -> bool:
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(str(d * 2)))
    return checksum % 10 == 0
