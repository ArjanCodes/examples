import enum
import hashlib
import re

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    SecretStr,
    ValidationError
)

VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")


class Role(enum.IntFlag):
    Author = 1
    Editor = 2
    Admin = 4
    SuperAdmin = 8


class User(BaseModel):
    name: str = Field(examples = ['Arjan'])
    email: EmailStr = Field(
            examples = ['user@arjancodes.com'],
            description = 'The email address of the user',
            frozen = True
    )
    password: SecretStr = Field(
            examples = ['Password123'],
            description = 'The password of the user')
    role: Role = Field(
            default = None,
            description = 'The role of the user',
            examples = [1, 2, 4, 8]
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v:str) -> str:
        if not VALID_NAME_REGEX.match(v):
            raise ValueError('Name is invalid, must contain only letters and be at least 2 characters long')
        return v

    @field_validator('role', mode = "before")
    @classmethod
    def validate_role(cls, v: int | str | Role) -> Role:
        op = {
                int : lambda x: Role(x),
                str : lambda x: Role[x],
                Role: lambda x: x
        }
        try:
            return op[type(v)](v)
        except (KeyError, ValueError):
            raise ValueError(f'Role is invalid, please use one of the following: {", ".join([x.name for x in Role])}')

    @model_validator(mode = "before")
    @classmethod
    def validate_user(cls, v:dict) -> dict:
        if "name" not in v or "password" not in v:
            raise ValueError('Name and password are required')
        if v['name'].casefold() in v['password'].casefold():
            raise ValueError('Password cannot contain name')
        if not VALID_PASSWORD_REGEX.match(v['password']):
            raise ValueError('Password is invalid, must contain 8 characters, 1 uppercase, 1 lowercase, 1 number')
        v['password'] = hashlib.sha256(v['password'].encode()).hexdigest()
        return v


def validate(data: dict) -> dict)):
    try:
        user = User.model_validate(data)
        print(user)
        return user
    except ValidationError as e:
        print('User is invalid:')
        print(e)
        return None


def main():
    for example_name, data in dict(
            good_data = {
                    'name'    : 'Arjan',
                    'email'   : 'example@arjancodes.com',
                    'password': 'Password123',
                    'role'    : 'Admin'
            },

            bad_role = {
                    'name'    : 'Arjan',
                    'email'   : 'example@arjancodes.com',
                    'password': 'Password123',
                    'role'    : 'Programmer'
            },

            bad_data = {
                    'name'    : 'Arjan',
                    'email'   : 'bad email',
                    'password': 'bad password',
            },

            bad_name = {
                    'name'    : 'Arjan<-_->',
                    'email'   : 'example@arjancodes.com',
                    'password': 'Password123',
            },

            duplicate = {
                    'name'    : 'Arjan',
                    'email'   : 'example@arjancodes.com',
                    'password': 'Arjan123',
            },

            missing_data = {
                    'email'   : '<bad data>',
                    'password': '<bad data>',
            }
    ).items():
        print(example_name)
        validate(data)
        print()


if __name__ == '__main__':
    main()
