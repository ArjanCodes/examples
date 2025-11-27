from abc import ABC, abstractmethod
from dataclasses import asdict, astuple, dataclass, field

# ================================================================
# USER DATACLASS WITH ALL FEATURES FROM THE VIDEO
# ================================================================


@dataclass(order=True, slots=True, kw_only=True, frozen=True)
class User:
    name: str
    email: str
    tags: list[str] = field(default_factory=list[str])
    slug: str = field(init=False)

    def __post_init__(self):
        # Normalize name and create slug
        normalized_name = self.name.strip().title()
        slugified = normalized_name.lower().replace(" ", "-")

        object.__setattr__(self, "name", normalized_name)
        object.__setattr__(self, "slug", slugified)

    @property
    def domain(self) -> str:
        """Return the domain part of the email address."""
        return self.email.split("@")[-1]

    def contact_card(self) -> str:
        """Return a formatted contact card."""
        return f"{self.name} <{self.email}>"

    @classmethod
    def from_email(cls, email: str) -> "User":
        """Create a User from only an email address."""
        local = email.split("@")[0].replace(".", " ")
        name = local.title()
        return cls(name=name, email=email)


# ================================================================
# ABSTRACT DATACLASS EXAMPLE
# ================================================================


@dataclass
class Account(ABC):
    owner: str
    base_fee: float

    @property
    @abstractmethod
    def monthly_fee(self) -> float: ...


@dataclass
class FreeAccount(Account):
    @property
    def monthly_fee(self) -> float:
        return 0.0


@dataclass
class PremiumAccount(Account):
    extra_storage_gb: int = 100

    @property
    def monthly_fee(self) -> float:
        return self.base_fee + (self.extra_storage_gb * 0.10)


# ================================================================
# MAIN WITH RUNNING EXAMPLES
# ================================================================


def main():
    print("\n=== Creating Users ===")
    u1 = User(name="alice", email="alice@example.com")
    u2 = User(name="bob", email="bob@example.com")
    print("u1:", u1)
    print("u2:", u2)

    print("\n=== Using from_email constructor ===")
    u3 = User.from_email("john.doe@company.com")
    print("u3:", u3)

    print("\n=== Comparing Users (order=True) ===")
    print("u1 < u2:", u1 < u2)
    print("Sorted:", sorted([u2, u1, u3]))

    print("\n=== Frozen Dataclass Behavior ===")
    try:
        u1.name = "Charlie"  # should fail
    except Exception as e:
        print("Attempting to reassign u1.name:", e)

    print("\n=== Shallow Immutability Example ===")
    u1.tags.append("admin")
    print("u1.tags after append:", u1.tags)

    print("\n=== Serialization ===")
    print("asdict(u1):", asdict(u1))
    print("astuple(u1):", astuple(u1))

    print("\n=== Account Types (Abstract Dataclasses) ===")
    free = FreeAccount(owner="Alice", base_fee=0)
    premium = PremiumAccount(owner="Bob", base_fee=5)
    print("FreeAccount monthly fee:", free.monthly_fee)
    print("PremiumAccount monthly fee:", premium.monthly_fee)


if __name__ == "__main__":
    main()
