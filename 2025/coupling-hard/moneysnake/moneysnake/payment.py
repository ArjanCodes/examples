from .model import MoneybirdModel


class Payment(MoneybirdModel):
    """
    Represents a payment in Moneybird.
    """

    payment_date: str | None = None
    price: float | None = None
    price_base: float | None = None
    financial_account_id: int | None = None
    financial_mutation_id: int | None = None
    manual_payment_action: str | None = "bank_transfer"
    transaction_identifier: str | None = None
    ledger_account_id: int | None = None
    invoice_id: int | None = None

    def save(self) -> None:
        raise NotImplementedError(
            "Payments cannot be saved directly. Refer to the invoice that the payment is for."
        )

    def delete(self) -> None:
        raise NotImplementedError(
            "Payments cannot be deleted directly. Refer to the invoice that the payment is for."
        )
