class BankAccount:
    def __init__(self, balance: int) -> None:
        self.balance = balance


def main() -> None:
    account = BankAccount(100)
    account.balance -= 50  # Direct modification
    account.balance += 100  # Direct modification
    print(account.balance)


if __name__ == "__main__":
    main()
