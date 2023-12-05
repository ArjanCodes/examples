from expressions import EMAIL_REGEX_BAD
from validator import validate_email


def main() -> None:
    email = "support@arjancodes.com"
    
    validate_email(EMAIL_REGEX_BAD, email)


if __name__ == "__main__":
    main()
