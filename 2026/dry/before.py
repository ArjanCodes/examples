def normalize_email_addresses(addresses: list[str]) -> list[str]:
    result: list[str] = []
    for address in addresses:
        address = address.strip().lower()
        if "@" not in address:
            continue
        local_part, domain = address.split("@", maxsplit=1)
        domain = domain.removeprefix("mail.")
        result.append(f"{local_part}@{domain}")
    return result


def normalize_usernames(usernames: list[str]) -> list[str]:
    result: list[str] = []
    for username in usernames:
        username = username.strip().lower()
        if len(username) < 3:
            continue
        username = username.removeprefix("@")
        result.append(username)
    return result


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
