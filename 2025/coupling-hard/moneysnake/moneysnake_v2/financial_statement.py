from typing import Any, Self
from pydantic import Field, field_validator

from .client import MoneybirdClient

from .model import MoneybirdModel
from .financial_mutation import FinancialMutation


class FinancialStatement(MoneybirdModel):
    """
    Represents a financial statement in Moneybird.
    """

    financial_account_id: str | None = None
    reference: str | None = None
    official_date: str | None = None
    official_balance: str | None = None
    importer_service: str | None = None
    financial_mutations: list[FinancialMutation] = Field(default_factory=list)

    @field_validator("financial_mutations")
    def ensure_financial_mutations(
        cls, value: list[dict[str, Any]] | None
    ) -> list[FinancialMutation] | None:
        if value is None:
            return None

        financial_mutations: list[FinancialMutation] = []

        for financial_mutation in value:
            if isinstance(financial_mutation, FinancialMutation):
                financial_mutations.append(financial_mutation)
            else:
                financial_mutations.append(FinancialMutation(**financial_mutation))

        return financial_mutations

    def save(self) -> None:
        """
        Save the external sales invoice. Overrides the save method in MoneybirdModel.
        """
        financial_statement_data = self.to_dict()

        # For the POST and PATCH requests we need to use the details_attributes key
        # instead of details key to match the Moneybird API.
        financial_statement_data["financial_mutations_attributes"] = (
            financial_statement_data.pop("financial_mutations", [])
        )

        if self.id is None:
            data = self.client.http_post(
                f"{self.endpoint}s",
                data={self.endpoint: financial_statement_data},
            )

        else:
            data = self.client.http_patch(
                f"{self.endpoint}s/{self.id}",
                data={self.endpoint: financial_statement_data},
            )
        self.update(data)

    def load(self, id: int) -> None:
        raise NotImplementedError(
            "Financial statements cannot be loaded from Moneybird."
        )

    def add_financial_mutation(self, financial_mutation: FinancialMutation) -> None:
        """
        Add a financial mutation to the financial statement.
        """
        self.financial_mutations.append(financial_mutation)

    @classmethod
    def find_by_id(cls: type[Self], client: MoneybirdClient, id: int) -> Self:
        raise NotImplementedError(
            "Financial statements cannot be loaded from Moneybird."
        )
