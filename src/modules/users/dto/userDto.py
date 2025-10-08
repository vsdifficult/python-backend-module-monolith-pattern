from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class User(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: int
    is_verify: bool

    class Config:
        orm_mode = True

class UserWithPassword(User):
    password: str

class RegisterUserDto(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: int

class LoginUserDto(BaseModel):
    email: EmailStr
    password: str

class UserDto(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: int
    is_verify: bool

