from dataclasses import dataclass

from user_repo import AccountStatus


@dataclass
class UserAccount:
    user_id: int
    _username: str
    _email: str
    _status: AccountStatus

    # ---- Methods for everything ----

    def get_username(self) -> str:
        return self._username

    def get_email(self) -> str:
        return self._email

    def get_status(self) -> AccountStatus:
        return self._status

    def is_active(self) -> bool:
        return self.get_status() is AccountStatus.ACTIVE


# ---- Demo ----


def main() -> None:
    account = UserAccount(
        user_id=101,
        _username="mason",
        _email="mason@arjancodes.com",
        _status=AccountStatus.ACTIVE,
    )

    print("Username:", account.get_username())
    print("Email:", account.get_email())
    print("Status:", account.get_status())
    print("Is active:", account.is_active())


if __name__ == "__main__":
    main()
