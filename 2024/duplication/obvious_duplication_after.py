def calculate_tax(employee_name: str, salary: float, tax_rate: float) -> None:
    """Calculate and print the tax for a given employee."""
    tax_amount = salary * tax_rate
    print(f"Tax for {employee_name} is: {tax_amount}")


def main() -> None:
    tax_rate = 0.2

    employees = [("Alice Jones", 65000), ("Bob Smith", 60000)]

    for name, salary in employees:
        calculate_tax(name, salary, tax_rate)


if __name__ == "__main__":
    main()
