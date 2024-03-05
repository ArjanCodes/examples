"""Add city and weather tables

Revision ID: 1d6ef8d6c1cf
Revises: 57065631a799
Create Date: 2024-03-06 13:33:28.244298

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1d6ef8d6c1cf"
down_revision: Union[str, None] = "57065631a799"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("population", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(op.f("ix_cities_id"), "cities", ["id"], unique=False)

    op.create_index(op.f("ix_cities_name"), "cities", ["name"], unique=False)

    op.create_table(
        "weather",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=True),
        sa.Column("temperature", sa.Integer(), nullable=True),
        sa.Column("humidity", sa.Integer(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["city_id"],
            ["cities.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_weather_id"), "weather", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_weather_id"), table_name="weather")
    op.drop_table("weather")
    op.drop_index(op.f("ix_cities_name"), table_name="cities")
    op.drop_index(op.f("ix_cities_id"), table_name="cities")
    op.drop_table("cities")
