

from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List

class PostDto(BaseModel):
    Id: UUID
    Name: str
    Tags: List[str]
    OwnerName: str
    OwnerId: UUID
    Image: Optional[str] 

class CreatePostDto(BaseModel):
    Name: str
    Tags: List[str]
    Image: Optional[str]

class UpdatePostDto(BaseModel):
    Name: Optional[str] = None
    Tags: Optional[List[str]] = None
    Image: Optional[str] = None
