from dataclasses import dataclass
from typing import Iterable

from rules import RuleFn, load_rule_from_config, rule

# ---------------------------------------------------------------------------
# DOMAIN MODEL
# ---------------------------------------------------------------------------


@dataclass
class User:
    is_admin: bool
    is_active: bool
    account_age: int
    is_banned: bool
    country: str
    credit_score: int
    has_manual_override: bool


# ---------------------------------------------------------------------------
# BUSINESS RULES (SIMPLY USE @predicate)
# ---------------------------------------------------------------------------


@rule
def is_admin() -> RuleFn[User]:
    return lambda u: u.is_admin


@rule
def is_active() -> RuleFn[User]:
    return lambda u: u.is_active


@rule
def is_banned() -> RuleFn[User]:
    return lambda u: u.is_banned


@rule
def has_override() -> RuleFn[User]:
    return lambda u: u.has_manual_override


@rule
def account_older_than(days: int) -> RuleFn[User]:
    return lambda u: u.account_age > days


@rule
def from_country(countries: Iterable[str]) -> RuleFn[User]:
    return lambda u: u.country in countries


@rule
def credit_score_above(threshold: int) -> RuleFn[User]:
    return lambda u: u.credit_score > threshold


# ---------------------------------------------------------------------------
# BUILD RULE IN PYTHON DSL
# ---------------------------------------------------------------------------

AccessRule = is_admin() | (
    is_active()
    & account_older_than(30)
    & ~is_banned()
    & from_country(["NL", "BE"])
    & (credit_score_above(650) | has_override())
)

# ---------------------------------------------------------------------------
# EXAMPLE SYSTEM USAGE
# ---------------------------------------------------------------------------


def api_check(user: User):
    return AccessRule(user)


def reporting(users: list[User]) -> list[User]:
    return [u for u in users if AccessRule(u)]


def cli_export(users: list[User]) -> list[User]:
    return [u for u in users if AccessRule(u)]


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------


def main() -> None:
    users = [
        User(True, False, 1, False, "US", 100, False),
        User(False, True, 40, False, "NL", 700, False),
        User(False, True, 40, False, "BE", 500, True),
        User(False, True, 5, False, "NL", 900, False),
        User(False, False, 100, True, "NL", 900, False),
    ]

    print("=== Access via Python DSL ===")
    for u in users:
        print(u, "=>", api_check(u))

    # If rule_config.json exists, load dynamic rule:
    try:
        DynamicRule = load_rule_from_config("rule_config.json")
        print("\n=== Access via Config Rule ===")
        for u in users:
            print(u, "=>", DynamicRule(u))
    except FileNotFoundError:
        print("\n(No rule_config.json found — skipping dynamic demo)")


if __name__ == "__main__":
    main()
