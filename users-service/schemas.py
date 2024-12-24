from validations import (
    validate_name,
    validate_email_address,
    validate_password,
    NAME_MIN_LENGTH,
    NAME_MAX_LENGTH
)
from pydantic import BaseModel, EmailStr, field_validator, Field

class UserLoginBase(BaseModel):
    email: str
    password: str

class CreateUserBase(BaseModel):
    first_name: str = Field(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, frozen=True)
    last_name: str = Field(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, frozen=True)
    email: EmailStr
    password: str

    # @field_validator("first_name")
    # @classmethod
    # def first_name_validator(cls, value):
    #     errors = validate_name("first_name", value)
    #     if len(errors):
    #         raise ValueError(errors[0])
    #     return value

    # @field_validator("last_name")
    # @classmethod
    # def last_name_validator(cls, value):
    #     errors = validate_name("last_name", value)
    #     if len(errors):
    #         raise ValueError(errors[0])
    #     return value

    @field_validator("password")
    @classmethod
    def password_validator(cls, value):
        errors = validate_password(value)
        if len(errors):
            raise ValueError(errors[0])
        return value