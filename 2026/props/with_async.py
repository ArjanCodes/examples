import asyncio
from dataclasses import dataclass

from user_repo import AccountStatus, InMemoryUserRepository, UserRepository


class BadUserAccount:
    def __init__(self, user_id: int, repo: UserRepository) -> None:
        self.user_id = user_id
        self._repo = repo

    @property
    async def username(self) -> str:
        # Looks cheap, but does I/O every time
        return await self._repo.fetch_username(self.user_id)

    @property
    async def is_active(self) -> bool:
        # Derived value that ALSO hides I/O
        status = await self._repo.fetch_status(self.user_id)
        return status is AccountStatus.ACTIVE


# ---- ✅ Better design: explicit async boundaries ----


@dataclass
class UserAccount:
    user_id: int
    username: str
    email: str
    status: AccountStatus

    @classmethod
    async def load(cls, user_id: int, repo: UserRepository) -> "UserAccount":
        username, email, status = await asyncio.gather(
            repo.fetch_username(user_id),
            repo.fetch_email(user_id),
            repo.fetch_status(user_id),
        )
        return cls(
            user_id=user_id,
            username=username,
            email=email,
            status=status,
        )

    @property
    def is_active(self) -> bool:
        return self.status is AccountStatus.ACTIVE

    async def save(self, repo: UserRepository) -> None:
        await asyncio.gather(
            repo.update_username(self.user_id, self.username),
            repo.update_email(self.user_id, self.email),
            repo.update_status(self.user_id, self.status),
        )


# ---- Demo ----


async def main() -> None:
    repo = InMemoryUserRepository()

    print("=== Bad design: async properties ===")
    bad = BadUserAccount(user_id=101, repo=repo)
    print("username (1):", await bad.username)
    print("username (2):", await bad.username, "(fetched twice)")
    print("is_active:", await bad.is_active)

    print("\n=== Better design: explicit load + save ===")
    account = await UserAccount.load(user_id=101, repo=repo)
    print("Loaded:", account)

    account.email = "new-email@arjancodes.com"
    await account.save(repo)

    reloaded = await UserAccount.load(user_id=101, repo=repo)
    print("Reloaded:", reloaded)

    print("\n=== create/delete demo ===")
    await repo.create_user(
        999,
        username="jordan",
        email="jordan@arjancodes.com",
        status=AccountStatus.ACTIVE,
    )
    created = await UserAccount.load(999, repo)
    print("Created:", created)

    await repo.delete_user(999)
    print("Deleted user 999")


if __name__ == "__main__":
    asyncio.run(main())
