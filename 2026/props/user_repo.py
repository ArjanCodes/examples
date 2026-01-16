import asyncio
from dataclasses import dataclass, replace
from enum import StrEnum
from typing import Protocol


class AccountStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"


@dataclass(frozen=True)
class UserRecord:
    username: str
    email: str
    status: AccountStatus


# ---- Repository abstraction ----


class UserRepository(Protocol):
    async def fetch_username(self, user_id: int) -> str: ...
    async def fetch_email(self, user_id: int) -> str: ...
    async def fetch_status(self, user_id: int) -> AccountStatus: ...

    async def update_username(self, user_id: int, username: str) -> None: ...
    async def update_email(self, user_id: int, email: str) -> None: ...
    async def update_status(self, user_id: int, status: AccountStatus) -> None: ...

    async def create_user(
        self,
        user_id: int,
        *,
        username: str,
        email: str,
        status: AccountStatus,
    ) -> None: ...

    async def delete_user(self, user_id: int) -> None: ...


# ---- Concrete repository (in-memory, async) ----


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[int, UserRecord] = {
            101: UserRecord(
                username="mason",
                email="mason@arjancodes.com",
                status=AccountStatus.ACTIVE,
            ),
            204: UserRecord(
                username="harper",
                email="harper@arjancodes.com",
                status=AccountStatus.SUSPENDED,
            ),
        }

    async def fetch_username(self, user_id: int) -> str:
        await asyncio.sleep(0.05)
        return self._users[user_id].username

    async def fetch_email(self, user_id: int) -> str:
        await asyncio.sleep(0.05)
        return self._users[user_id].email

    async def fetch_status(self, user_id: int) -> AccountStatus:
        await asyncio.sleep(0.05)
        return self._users[user_id].status

    async def update_username(self, user_id: int, username: str) -> None:
        await asyncio.sleep(0.05)
        self._users[user_id] = replace(
            self._users[user_id],
            username=username,
        )

    async def update_email(self, user_id: int, email: str) -> None:
        await asyncio.sleep(0.05)
        self._users[user_id] = replace(
            self._users[user_id],
            email=email,
        )

    async def update_status(self, user_id: int, status: AccountStatus) -> None:
        await asyncio.sleep(0.05)
        self._users[user_id] = replace(
            self._users[user_id],
            status=status,
        )

    async def create_user(
        self,
        user_id: int,
        *,
        username: str,
        email: str,
        status: AccountStatus,
    ) -> None:
        await asyncio.sleep(0.05)
        self._users[user_id] = UserRecord(
            username=username,
            email=email,
            status=status,
        )

    async def delete_user(self, user_id: int) -> None:
        await asyncio.sleep(0.05)
        del self._users[user_id]
