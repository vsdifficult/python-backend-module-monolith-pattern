from pydantic import BaseModel 
from uuid import UUID, uuid4

class UserDto(BaseModel): 
    Id: UUID
    emial: str 
    name: str 
    password: str 
    role: int 
    code: int 
    isVerify: bool 

class RegisterUserDto(BaseModel): 
    name: str
    email: str
    password: str 
    role: int  
