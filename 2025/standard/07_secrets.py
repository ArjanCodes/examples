import secrets

def main() -> None:
    # Generate a secure hexadecimal token
    token_hex: str = secrets.token_hex(16)
    print("Secure hex token:", token_hex)

    # Generate a secure URL-safe token
    token_url: str = secrets.token_urlsafe(16)
    print("Secure URL-safe token:", token_url)

    # Generate random bytes
    random_bytes: bytes = secrets.token_bytes(16)
    print("Random bytes:", random_bytes)

    # Randomly choose an item from a sequence
    choices = ["apple", "banana", "cherry"]
    selected: str = secrets.choice(choices)
    print("Random choice:", selected)

if __name__ == "__main__":
    main()