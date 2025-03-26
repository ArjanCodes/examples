from dataclasses import dataclass
from enum import StrEnum, auto


@dataclass
class Account:
    owner: str
    _balance: int = 0

    def deposit(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        print(f"Deposited: {amount}.")

    def withdraw(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient balance.")
        self._balance -= amount
        print(f"Withdrew: {amount}.")

    @property
    def balance(self) -> int:
        return self._balance


class PaymentType(StrEnum):
    CASH = auto()
    CARD = auto()
    TRANSFER = auto()


SERVICE_FEES = {
    PaymentType.CASH: 50,
    PaymentType.CARD: 100,
    PaymentType.TRANSFER: 150,
}


def pay_service_fee(account: Account, payment_type: PaymentType) -> None:
    account._balance -= SERVICE_FEES[payment_type]
    print(f"Service fee paid using {payment_type}.")


def main() -> None:
    account = Account("John Doe", 1000)
    account.deposit(500)
    print(f"Balance after deposit: {account.balance}.")

    pay_service_fee(account, PaymentType.CARD)
    print(f"Balance after paying the service fee: {account.balance}.")


if __name__ == "__main__":
    main()
