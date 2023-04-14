from dataclasses import dataclass
from email.message import EmailMessage
from smtplib import SMTP_SSL

SMTP_SERVER = "smtp.gmail.com"
PORT = 465
EMAIL = "hi@arjancodes.com"
PASSWORD = "password"


@dataclass
class Person:
    name: str
    age: int
    address_line_1: str
    address_line_2: str
    city: str
    country: str
    postal_code: str
    email: str
    phone_number: str
    gender: str
    height: float
    weight: float
    blood_type: str
    eye_color: str
    hair_color: str

    def split_name(self) -> tuple[str, str]:
        first_name, last_name = self.name.split(" ")
        return first_name, last_name

    def get_full_address(self) -> str:
        return f"{self.address_line_1}, {self.address_line_2}, {self.city}, {self.country}, {self.postal_code}"

    def get_bmi(self) -> float:
        return self.weight / (self.height**2)

    def get_bmi_category(self) -> str:
        if self.get_bmi() < 18.5:
            return "Underweight"
        elif self.get_bmi() < 25:
            return "Normal"
        elif self.get_bmi() < 30:
            return "Overweight"
        else:
            return "Obese"

    def update_email(self, email: str) -> None:
        self.email = email
        # send email to the new address
        msg = EmailMessage()
        msg.set_content(
            "Your email has been updated. If this was not you, you have a problem."
        )
        msg["Subject"] = "Your email has been updated."
        msg["To"] = self.email

        with SMTP_SSL(SMTP_SERVER, PORT) as server:
            # server.login(EMAIL, PASSWORD)
            # server.send_message(msg, EMAIL)
            pass
        print("Email sent successfully!")


def main() -> None:
    # create a person
    person = Person(
        name="John Doe",
        age=30,
        address_line_1="123 Main St",
        address_line_2="Apt 1",
        city="New York",
        country="USA",
        postal_code="12345",
        email="johndoe@gmail.com",
        phone_number="123-456-7890",
        gender="Male",
        height=1.8,
        weight=80,
        blood_type="A+",
        eye_color="Brown",
        hair_color="Black",
    )

    # compute the BMI
    bmi = person.get_bmi()
    print(f"Your BMI is {bmi:.2f}")
    print(f"Your BMI category is {person.get_bmi_category()}")

    # update the email address
    person.update_email("johndoe@outlook.com")


if __name__ == "__main__":
    main()
