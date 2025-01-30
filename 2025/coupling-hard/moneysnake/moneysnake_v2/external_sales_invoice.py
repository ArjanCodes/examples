from pydantic import Field, field_validator
from typing import Any, cast

from pydantic import BaseModel

from .model import MoneybirdModel
from .client import http_delete, http_get, http_patch, http_post
from .payment import Payment


class ExternalSalesInvoiceDetailsAttribute(BaseModel):
    """
    Details attribute for an external sales invoice.
    """

    id: int | None = None
    description: str | None = None
    period: str | None = None
    price: int | None = None
    amount: int | str | None = None
    tax_rate_id: int | None = None
    ledger_account_id: str | None = None
    project_id: str | None = None

    def update(self, data: dict[str, Any]) -> None:
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


# External sales invoices don't have custom fields, so we use MoneybirdModel
# instead of CustomFieldModel.


class ExternalSalesInvoice(MoneybirdModel):
    """
    Represents an external sales invoice in Moneybird.
    """

    contact_id: int | None = None
    reference: str | None = None
    date: str | None = None
    due_date: str | None = None
    currency: str | None = None
    prices_are_incl_tax: bool | None = None
    source: str | None = None
    source_url: str | None = None
    details: list[ExternalSalesInvoiceDetailsAttribute] | None = Field(
        default_factory=list
    )
    payments: list[Payment] | None = Field(default_factory=list)

    @field_validator("payments")
    def ensure_payments(
        cls, value: list[dict[str, Any]] | None
    ) -> list[Payment] | None:
        if value is None:
            return None

        return [Payment(**payment) for payment in value]

    def update(self, data: dict[str, Any]) -> None:
        """
        Update the external sales invoice. Overrides the update method in MoneybirdModel.
        """
        super().update(data)
        if self.payments is not None:
            pass
            # self.payments = [
            #     Payment.model_dump(p) if isinstance(p, dict) else p for p in self.payments
            # ]

    def save(self) -> None:
        """
        Save the external sales invoice. Overrides the save method in MoneybirdModel.
        """
        invoice_data = self.to_dict()
        # For the POST and PATCH requests we need to use the details_attributes key
        # instead of details key to match the Moneybird API.
        invoice_data["details_attributes"] = invoice_data.pop("details", [])

        if self.id is None:
            data = http_post(
                f"{self.endpoint}s",
                data={self.endpoint: invoice_data},
            )
        else:
            data = http_patch(
                f"{self.endpoint}s/{self.id}",
                data={self.endpoint: invoice_data},
            )
        self.update(data)

    def add_detail(self, detail: ExternalSalesInvoiceDetailsAttribute) -> None:
        """
        Add a detail to the external sales invoice.
        """
        if self.details is None:
            self.details = []

        self.details.append(detail)

    def get_detail(self, detail_id: int) -> ExternalSalesInvoiceDetailsAttribute:
        """
        Get a detail from the external sales invoice.
        """

        if not self.details:
            raise ValueError("No details found.")

        for detail in self.details:
            if detail.id == detail_id:
                return detail
        raise ValueError(f"Detail with id {detail_id} not found.")

    def update_detail(
        self, detail_id: int, data: dict[str, Any]
    ) -> ExternalSalesInvoiceDetailsAttribute:
        """
        Update a detail from the external sales invoice.
        """
        detail = self.get_detail(detail_id)
        detail.update(data)
        return detail

    def delete_detail(self, detail_id: int) -> None:
        """
        Delete a detail from the external sales invoice.
        """

        if self.details:
            self.details = [detail for detail in self.details if detail.id != detail_id]

    def list_all_by_contact_id(
        self,
        contact_id: int,
        state: str | None = "all",
        period: str | None = "this_year",
    ) -> list["ExternalSalesInvoice"]:
        """
        List all external sales invoices for a contact.
        """
        data = http_get(
            path=f"{self.endpoint}s/?filter=contact_id:{contact_id}&state:{state}&period:{period}"
        )

        data_list = cast(list[dict[str, Any]], data)

        invoices: list[ExternalSalesInvoice] = []
        for invoice_data in data_list:
            invoice_obj = ExternalSalesInvoice(**invoice_data)
            invoices.append(invoice_obj)
        return invoices

    def create_payment(self, payment: Payment) -> None:
        """
        Create a payment for the external sales invoice.
        """
        data = http_post(
            path=f"{self.endpoint}s/{self.id}/payments",
            data={"payment": payment.to_dict()},
        )
        # Get the payment data from the response and append it to the payments list
        payment_data = data.get("payment")

        if self.payments is None:
            self.payments = []

        if payment_data:
            self.payments.append(Payment(**payment_data))

    def delete_payment(self, payment_id: int) -> None:
        """
        Delete a payment for the external sales invoice.
        """
        http_delete(
            path=f"{self.endpoint}s/{self.id}/payments/{payment_id}",
        )

        if not self.payments:
            raise ValueError("No payments found.")

        self.payments = [
            payment for payment in self.payments if payment.id != payment_id
        ]
