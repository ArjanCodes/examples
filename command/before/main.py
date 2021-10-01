from banking.bank import Bank


def main() -> None:

    # create a bank
    bank = Bank()

    # create some accounts
    account1 = bank.create_account("Arjan Codes")
    account2 = bank.create_account("Google")
    account3 = bank.create_account("Microsoft")

    print(bank)


if __name__ == "__main__":
    main()
