from src.kernel.models.baseModel import Base 

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, ARRAY, UUID
from sqlalchemy import String

import uuid 

class PostEntity(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=True)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    image = Column(String, nullable=True)

    owner = relationship("UserEntity", back_populates="posts")