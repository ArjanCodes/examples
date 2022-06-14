from typing import Callable

import dash

DashCallbackRegistrant = Callable[[dash.Dash], None]


def register_callbacks(app: dash.Dash) -> None:
    for callback_registrant in collect_callback_registrants():
        callback_registrant(app)


def collect_callback_registrants() -> tuple[DashCallbackRegistrant, ...]:
    from . import (
        filter_budget_records,
        select_all_categories,
        select_all_months,
        select_all_years,
        update_pie_chart,
    )

    return (
        filter_budget_records.register,
        select_all_categories.register,
        select_all_months.register,
        select_all_years.register,
        update_pie_chart.register,
    )
