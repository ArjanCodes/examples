from banking.bank import Bank


def main() -> None:
    # create a bank
    bank = Bank()

    # create some accounts
    account1 = bank.create_account("ArjanCodes")
    account2 = bank.create_account("Google")
    account3 = bank.create_account("Microsoft")

    account1.deposit(100000)
    account2.deposit(100000)
    account3.deposit(100000)

    # transfer
    account2.withdraw(50000)
    account1.deposit(50000)

    account1.withdraw(150000)

    print(bank)


if __name__ == "__main__":
    main()
