from src.kernel.models.baseModel import Base 
from src.kernel.enums.roles import Role 
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, UUID
from sqlalchemy import String

import uuid 

class UserEntity(Base): 

    __tablename__ = "Users" 

    id = Column(UUID, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default=Role.User.value, nullable=False)
    code = Column(Integer, nullable=True) 
    isVerify = Column(Boolean, default=False)

