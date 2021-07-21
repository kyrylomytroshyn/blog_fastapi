from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: str
    name: str


class CreateUserParams(BaseModel):
    username: str
    name: str
    email: EmailStr
    phone: str
