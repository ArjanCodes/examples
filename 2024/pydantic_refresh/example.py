import re
from enum import auto, IntFlag

from pydantic import (
    BaseModel, 
    EmailStr, 
    Field, 
    field_validator, 
    SecretStr, 
    ValidationError
)
class Role(IntFlag):
    Author = auto()
    Editor = auto()
    Developer = auto()
    Admin = Author | Editor | Developer


class User(BaseModel):
    name: str = Field(examples=['Arjan'])
    email: EmailStr = Field(examples=['example@arjancodes.com'], description='The email address of the user', frozen = True)
    password: SecretStr = Field(examples=['Password123'], description='The password of the user')
    role: Role = Field(default=None,  description='The role of the user')

def validate(data: dict) -> User:
    try:
        user = User.model_validate(data)
        print(user)
    except ValidationError as e:
        print('User is invalid')
        for error in e.errors():
            print(error)
        
def main():
    good_data = {
        'name': 'Arjan',
        'email': 'example@arjancodes.com',
        'password': 'Password123'
    }
    
    bad_data = {
        'email': '<bad data>',
        'password': '<bad data>'
    }

    validate(good_data)

    validate(bad_data)


if __name__ == '__main__':
    main()