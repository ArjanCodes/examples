def is_valid_email(address: str) -> bool:
    address = address.strip().lower()
    return "@" in address


def normalize_email(address: str) -> str:
    address = address.strip().lower()
    local_part, domain = address.split("@", maxsplit=1)
    domain = domain.removeprefix("mail.")
    return f"{local_part}@{domain}"


def is_valid_username(username: str) -> bool:
    username = username.strip().lower()
    return len(username) >= 3


def normalize_username(username: str) -> str:
    username = username.strip().lower()
    return username.removeprefix("@")


def normalize_email_addresses(addresses: list[str]) -> list[str]:
    return [normalize_email(a) for a in addresses if is_valid_email(a)]


def normalize_usernames(usernames: list[str]) -> list[str]:
    return [normalize_username(u) for u in usernames if is_valid_username(u)]


def main() -> None:
    email_addresses = [
        "Example@Mail.arjancodes.com",
        "Test@hotmail.com",
        "User@live.com",
        "not-an-email",
    ]
    normalized_emails = normalize_email_addresses(email_addresses)
    print(normalized_emails)

    usernames = [" @ExampleUser ", " @TestUser ", " @User ", " @U "]
    normalized_usernames = normalize_usernames(usernames)
    print(normalized_usernames)


if __name__ == "__main__":
    main()
