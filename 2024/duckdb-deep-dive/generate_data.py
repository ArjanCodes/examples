import csv
from faker import Faker
import random
from pathlib import Path
import argparse


def generate_employee_csv(file_name: str, num_employees: int) -> None:
    # Initialize Faker
    fake = Faker()

    # Define possible job positions
    job_positions = [
        "Software Engineer",
        "Data Scientist",
        "Product Manager",
        "HR Specialist",
        "Marketing Coordinator",
    ]

    # Open the file for writing
    output_file = Path(file_name)
    with output_file.open(mode="w", newline="") as csvfile:
        fieldnames = ["Employee Name", "Job Position", "Salary"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Generate employee data
        for _ in range(num_employees):
            writer.writerow(
                {
                    "name": fake.name(),
                    "position": random.choice(job_positions),
                    "salary": round(
                        random.uniform(50_000, 150_000), 2
                    ),  # Salary range between 50,000 and 150,000
                }
            )

    print(f"Generated {num_employees} employee records in '{file_name}'.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a CSV file with employee data."
    )
    parser.add_argument(
        "file_name",
        type=str,
        help="The name of the output CSV file.",
        default="employees.csv",
    )
    parser.add_argument(
        "num_employees", type=int, help="The number of employee records to generate."
    )

    args = parser.parse_args()

    generate_employee_csv("./data" + args.file_name, args.num_employees)


if __name__ == "__main__":
    main()
