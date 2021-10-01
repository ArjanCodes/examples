from banking.bank import Bank
from banking.controller import BankController
from banking.transactions import Deposit, Transfer, Withdrawal


def main() -> None:

    # create a bank
    bank = Bank()

    # create a bank controller
    controller = BankController()

    # create some accounts
    account1 = bank.create_account("Arjan Codes")
    account2 = bank.create_account("Google")
    account3 = bank.create_account("Microsoft")

    # deposit some money in my account
    controller.execute(Deposit(account1.number, 100000, bank))
    controller.undo()
    controller.redo()

    # more deposits
    controller.execute(Deposit(account2.number, 100000, bank))
    controller.execute(Deposit(account3.number, 100000, bank))

    # do a transfer
    controller.execute(Transfer(account2.number, account1.number, 50000, bank, bank))

    # undo and redo
    controller.undo()
    controller.undo()
    controller.redo()
    controller.redo()

    # get the money out of my account
    controller.execute(Withdrawal(account1.number, 150000, bank))

    print(bank)


if __name__ == "__main__":
    main()
