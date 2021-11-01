from banking.bank import Bank
from banking.commands import Batch, Deposit, Transfer, Withdrawal
from banking.controller import BankController


def main() -> None:

    # create a bank
    bank = Bank()

    # create a bank controller
    controller = BankController()

    # create some accounts
    account1 = bank.create_account("ArjanCodes")
    account2 = bank.create_account("Google")
    account3 = bank.create_account("Microsoft")

    # deposit some money in my account
    controller.register(Deposit(account1, 100000))
    controller.undo()
    controller.redo()

    # execute a batch of commands
    controller.register(
        Batch(
            commands=[
                Deposit(account2, 100000),
                Deposit(account3, 100000),
                # Withdrawal(account1, 100000000),
                Transfer(account2, account1, 50000),
            ]
        )
    )

    # undo and redo
    controller.undo()
    controller.undo()
    controller.redo()
    controller.redo()

    # get the money out of my account
    controller.register(Withdrawal(account1, 150000))

    # clear the cache and compute the balances
    bank.clear_cache()
    controller.compute_balances()

    print(bank)


if __name__ == "__main__":
    main()
