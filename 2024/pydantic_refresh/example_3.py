import enum
import hashlib
import re
from typing import Union

from pydantic import (BaseModel, EmailStr, Field, field_serializer, field_validator, model_serializer, model_validator,
                      SecretStr)

VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")


class Role(enum.IntFlag):
    User = 0
    Author = 1
    Editor = 2
    Admin = 4
    SuperAdmin = 8


class User(BaseModel):
    name: str = Field(examples = ['Example'])
    email: EmailStr = Field(
            examples = ['user@arjancodes.com'],
            description = 'The email address of the user',
            frozen = True
    )
    password: SecretStr = Field(
            examples = ['Password123'],
            description = 'The password of the user',
            exclude = True
    )
    role: Role = Field(
            description = 'The role of the user',
            examples = [1, 2, 4, 8],
            default = 0,
            validate_default = True
    )

    @field_validator('name')
    def validate_name(cls, v):
        if not VALID_NAME_REGEX.match(v):
            raise ValueError('Name is invalid, must contain only letters and be at least 2 characters long')
        return v

    @field_validator('role', mode = "before")
    @classmethod
    def validate_role(cls, v: Union[int, str, Role]):
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
    def validate_user_pre(cls, v):
        if "name" not in v or "password" not in v:
            raise ValueError('Name and password are required')
        if v['name'].casefold() in v['password'].casefold():
            raise ValueError('Password cannot contain name')
        if not VALID_PASSWORD_REGEX.match(v['password']):
            raise ValueError('Password is invalid, must contain 8 characters, 1 uppercase, 1 lowercase, 1 number')
        v['password'] = hashlib.sha256(v['password'].encode()).hexdigest()
        return v

    @model_validator(mode = "after")
    def validate_user_post(self, v):
        if self.role == Role.Admin and self.name != 'Arjan':
            raise ValueError('Only Arjan can be an admin')
        return self

    @field_serializer("role", when_used = "json")
    @classmethod
    def serialize_role(cls, v):
        return v.name

    @model_serializer(mode = "wrap", when_used = "json")
    def serialize_user(self, serializer, info) -> dict:
        if not info.include and not info.exclude:
            return {
                    'name': self.name,
                    'role': self.role.name
            }
        return serializer(self)


def main():
    data = {
            'name'    : 'Arjan',
            'email'   : 'example@arjancodes.com',
            'password': 'Password123',
            'role'    : 'Admin'
    }
    user = User.model_validate(data)
    if user:
        print("The serializer that returns a dict:", user.model_dump(), sep = '\n', end = '\n\n')
        print("The serializer that returns a JSON string:", user.model_dump(mode = 'json'), sep = '\n', end = '\n\n')
        print(
                "The serializer that returns a json string, excluding the role:",
                user.model_dump(exclude = ['role'], mode = 'json'),
                sep = '\n', end = '\n\n'
        )
        print("The serializer that encodes all values to a dict:", dict(user), sep = '\n')
        


if __name__ == '__main__':
    main()
