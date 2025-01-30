from dataclasses import dataclass


@dataclass
class Account:
    owner: str
    _balance: int = 0

    def deposit(self, amount: int) -> None:
        if amount > 0:
            self._balance += amount
            print(f"Deposited: {amount}")
        else:
            print("Deposit amount must be positive")

    def withdraw(self, amount: int) -> None:
        if 0 < amount <= self._balance:
            self._balance -= amount
            print(f"Withdrew: {amount}")
        else:
            print("Invalid withdrawal amount")

    def get_balance(self) -> int:
        return self._balance


def pay_service_fee(account: Account) -> None:
    if account.get_balance() > 0:
        account.withdraw(100)
        print("Manipulated Account: 100 deducted")


def main() -> None:
    account = Account("John Doe", 1000)
    account.deposit(500)
    print(f"Balance after deposit: {account.get_balance()}")

    pay_service_fee(account)
    print(f"Balance after manipulation: {account.get_balance()}")


if __name__ == "__main__":
    main()
