def normalize_strings(
    items: list[str],
    require_at_symbol: bool = False,
    min_length: int = 0,
    remove_prefix: str = "",
    strip_mail_prefix: bool = False,
    split_at_symbol: bool = False,
    lowercase: bool = True,
    strip_whitespace: bool = True,
) -> list[str]:
    result: list[str] = []

    for item in items:
        if strip_whitespace:
            item = item.strip()
        if lowercase:
            item = item.lower()
        if require_at_symbol and "@" not in item:
            continue
        if len(item) < min_length:
            continue
        if remove_prefix:
            item = item.removeprefix(remove_prefix)
        if split_at_symbol:
            local_part, domain = item.split("@", maxsplit=1)
            if strip_mail_prefix:
                domain = domain.removeprefix("mail.")
            item = f"{local_part}@{domain}"
        result.append(item)

    return result


def main() -> None:
    email_addresses = [
        "Example@Mail.arjancodes.com",
        "Test@hotmail.com",
        "User@live.com",
        "not-an-email",
    ]
    normalized_emails = normalize_strings(
        email_addresses,
        require_at_symbol=True,
        split_at_symbol=True,
        strip_mail_prefix=True,
    )
    print(normalized_emails)

    usernames = [" @ExampleUser ", " @TestUser ", " @User ", " @U "]
    normalized_usernames = normalize_strings(
        usernames,
        min_length=3,
        remove_prefix="@",
    )
    print(normalized_usernames)


if __name__ == "__main__":
    main()
