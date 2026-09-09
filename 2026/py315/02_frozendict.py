"""PEP 814: immutable, hashable mappings are now built in."""


def main() -> None:
    production = frozendict(host="api.example.com", retries=3)
    same_values_different_order = frozendict(retries=3, host="api.example.com")

    # This makes a useful configuration key, unlike an ordinary dict.
    clients_by_config = {production: "production client"}

    print(production)
    print(
        f"equal regardless of insertion order? {production == same_values_different_order}"
    )
    print(f"usable as a dictionary key? {clients_by_config[production]}")

    try:
        production["retries"] = 4
    except TypeError as error:
        print(f"mutation is rejected: {error}")


if __name__ == "__main__":
    main()
