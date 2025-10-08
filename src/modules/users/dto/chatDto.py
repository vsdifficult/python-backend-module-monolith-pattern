from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class MessageDto(BaseModel):
    id: UUID
    sender_id: UUID
    content: str
    created_at: datetime

class ChatDto(BaseModel):
    id: UUID
    title: str
    sender_id: UUID
    recipient_id: UUID
    messages: Optional[List[MessageDto]] = []
