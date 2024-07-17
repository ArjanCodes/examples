class BankAccount:
    def __init__(self, balance: int) -> None:
        self._balance = balance

    def get_balance(self) -> int:
        return self._balance

    def withdraw(self, amount: int) -> None:
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount


def main() -> None:
    account = BankAccount(100)
    account.withdraw(50)
    print(account.get_balance())


if __name__ == "__main__":
    main()
