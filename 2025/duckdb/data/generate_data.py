import csv
import random
from pathlib import Path

from faker import Faker


def generate_employee_csv(file_name: str, num_employees: int) -> None:
    # Initialize Faker
    fake = Faker()

    # Define possible job positions
    job_positions = [
        "Software Engineer",
        "Data Scientist",
        "Product Manager",
        "HR Specialist",
        "Marketing Manager",
    ]

    # Open the file for writing
    output_file = Path(file_name)
    with output_file.open(mode="w", newline="") as csvfile:
        fieldnames = ["name", "job_title", "salary"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Generate employee data
        for _ in range(num_employees):
            writer.writerow(
                {
                    "name": fake.name(),
                    "job_title": random.choice(job_positions),
                    "salary": int(
                        random.uniform(50_000, 150_000)
                    ),  # Salary range between 50,000 and 150,000
                }
            )

    print(f"Generated {num_employees} employee records in '{file_name}'.")


def main() -> None:
    num_employees = 20
    file_name = "employees.csv"

    generate_employee_csv("./data/" + file_name, num_employees)


if __name__ == "__main__":
    main()
