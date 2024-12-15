from pydantic import BaseModel

class UserLoginBase(BaseModel):
    email: str
    password: str

class CreateUserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str