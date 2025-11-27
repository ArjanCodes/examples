"""
BEFORE version — messy, duplicated, inconsistent business rules.

We pretend that three different parts of the system
(API endpoint, report builder, CLI export) all need to check
whether a user has access to a premium feature.

Each part implements the rule slightly differently.
"""

from dataclasses import dataclass


@dataclass
class User:
    id: int
    is_admin: bool
    is_active: bool
    account_age: int
    is_banned: bool
    country: str
    credit_score: int
    has_manual_override: bool


# -------------------------------------------------------------------------
# API CHECK — deep nesting, hard to follow
# -------------------------------------------------------------------------


def api_can_access(user: User) -> bool:
    if user.is_admin:
        return True

    if user.is_active and user.account_age > 30:
        if not user.is_banned:
            if user.country in {"NL", "BE"}:
                if user.credit_score > 650 or user.has_manual_override:
                    return True

    return False


# -------------------------------------------------------------------------
# REPORT BUILDER — duplicated logic, but slightly different
# (forgot to check country; used >= instead of >)
# -------------------------------------------------------------------------


def report_can_access(user: User) -> bool:
    if user.is_admin:
        return True

    if user.is_active:
        if user.account_age >= 30:  # subtle bug: >= vs >
            if not user.is_banned:
                # forgot country check entirely
                if user.credit_score > 650 or user.has_manual_override:
                    return True

    return False


# -------------------------------------------------------------------------
# CLI EXPORT — another version, because of course
# (forgot override check; added "DE" because someone assumed EU == OK)
# -------------------------------------------------------------------------


def cli_can_access(user: User) -> bool:
    if user.is_admin:
        return True

    if user.is_active and user.account_age > 30 and not user.is_banned:
        if user.country in {"NL", "BE", "DE"}:  # accidental extra country
            if user.credit_score > 650:  # forgot override
                return True

    return False


# -------------------------------------------------------------------------
# Demo: show discrepancies
# -------------------------------------------------------------------------


def main() -> None:
    user = User(
        id=1,
        is_admin=False,
        is_active=True,
        account_age=35,
        is_banned=False,
        country="NL",
        credit_score=600,
        has_manual_override=True,
    )

    print("API says:     ", api_can_access(user))
    print("Report says:  ", report_can_access(user))
    print("CLI says:     ", cli_can_access(user))


if __name__ == "__main__":
    main()
