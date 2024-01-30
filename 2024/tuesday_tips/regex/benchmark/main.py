from expressions import EMAIL_REGEX_1
from validator import validate_email


def main() -> None:
    email = "support@arjancodes.com"
    
    validate_email(EMAIL_REGEX_1, email)


if __name__ == "__main__":
    main()
