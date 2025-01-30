from typing import Any, Self
from pydantic import Field
from enum import Enum, auto

from .model import MoneybirdModel
from .client import MoneybirdClient


class LinkBookingType(Enum):
    """
    Enum for the different types of bookings that can be linked to a financial mutation.
    """

    LedgerAccount = auto()
    SalesInvoice = auto()
    Document = auto()
    PaymentTransactionBatch = auto()
    PurchaseTransaction = auto()
    NewPurchaseInvoice = auto()
    NewReceipt = auto()
    PaymentTransaction = auto()
    PurchaseTransactionBatch = auto()
    ExternalSalesInvoice = auto()
    Payment = auto()
    VatDocument = auto()


class UnlinkBookingType(Enum):
    """
    Enum for the different types of bookings that can be unlinked from a financial mutation.
    """

    LedgerAccountBooking = auto()
    Payment = auto()


class FinancialMutation(MoneybirdModel):
    """
    Represents a financial mutation in Moneybird.
    """

    id: int | None = None
    administration_id: str | int | None = None
    amount: str | None = None
    code: str | None = None
    date: str | None = None
    message: str | None = None
    contra_account_name: str | None = None
    contra_account_number: str | None = None
    state: str | None = None
    amount_open: str | None = None
    sepa_fields: str | None = None
    batch_reference: str | None = None
    financial_account_id: str | None = None
    currency: str | None = None
    original_amount: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    version: str | int | None = None
    financial_statement_id: str | None = None
    processed_at: str | None = None
    account_servicer_transaction_id: str | None = None
    payments: list[Any] = Field(default_factory=list)
    ledger_account_bookings: list[Any] = Field(default_factory=list)

    # Disable create, update and delete methods for financial mutations as they don't
    # exist in the Moneybird API.
    def save(self) -> None:
        raise NotImplementedError("Financial mutations cannot be saved in Moneybird.")

    def delete(self) -> None:
        raise NotImplementedError("Financial mutations cannot be deleted in Moneybird.")

    def book_payment(
        self,
        price_base: float,
        booking_id: int,
        booking_type: LinkBookingType = LinkBookingType.LedgerAccount,
    ) -> None:
        """
        Book a payment on this financial mutation.
        """
        self.client.http_patch(
            f"financial_mutations/{self.id}/link_booking",
            {
                "price_base": price_base,
                "booking_id": booking_id,
                "booking_type": booking_type.name,
            },
        )

    def remove_payment(
        self,
        booking_id: int,
        booking_type: UnlinkBookingType = UnlinkBookingType.LedgerAccountBooking,
    ) -> None:
        """
        Remove a payment from this financial mutation.
        """
        self.client.http_patch(
            f"financial_mutations/{self.id}/unlink_booking",
            {"booking_id": booking_id, "booking_type": booking_type.name},
        )

    @classmethod
    def update_by_id(
        cls: type[Self], client: MoneybirdClient, id: int, data: dict[str, Any]
    ) -> Self:
        raise NotImplementedError("Financial mutations cannot be updated in Moneybird.")

    @classmethod
    def delete_by_id(cls: type[Self], client: MoneybirdClient, id: int) -> Self:
        raise NotImplementedError("Financial mutations cannot be deleted in Moneybird.")
