def main() -> None:
    tax_rate = 0.2

    alice_name = "Alice Jones"
    alice_salary = 65000
    alice_tax_amount = alice_salary * tax_rate
    print(f"Tax for {alice_name} is: {alice_tax_amount}")

    bob_name = "Bob Smith"
    bob_salary = 60000
    bob_tax_amount = bob_salary * tax_rate
    print(f"Tax for {bob_name} is: {bob_tax_amount}")


if __name__ == "__main__":
    main()
