
from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4

import logging
import random

from sqlalchemy.future import select 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.modules.users.entities.userEntity import UserEntity
from src.modules.users.dto.userDto import RegisterUserDto

logger = logging.getLogger(__name__)

class UserRepository: 
    """Repository for working with UserEntity."""

    async def create_user(
        self, session: AsyncSession, user: RegisterUserDto
    ) -> Optional[UUID]:
        """
        Create new user in database.

        Args:
            session (AsyncSession): active SQLAlchemy session
            user (RegisterUserDto): DTO with user data

        Returns:
            UUID | None: User id if created successfully, otherwise None
        """
        entity = UserEntity(
            id=uuid4(), 
            email=user.email,
            name=user.name,
            password=self._hash_password(user.password),
            role=user.role,
            code=self._generate_confirmation_code(),
        )

        try:
            async with session.begin(): 
                session.add(entity)
            await session.refresh(entity)
            logger.info("User created successfully: %s", entity.id)
            return entity.id
        except SQLAlchemyError as e:
            logger.error("Failed to create user: %s", e, exc_info=True)
            await session.rollback()
            return None

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[UserEntity]:
        """Find user by email."""
        result = await session.execute(
            select(UserEntity).filter(UserEntity.email == email)
        )
        return result.scalar_one_or_none()

    async def delete_user(
        self, session: AsyncSession, id: UUID
        ) -> Optional[bool]:  
        """
        Delete user  

        Args: 
            session (AsyncSession): active SQLAlchemy session 
            id (UUID): user id  
        
        Returns: 
            True | False: True if deleted successfully, otherwise False
        """
        entity = await session.execute(
            select(UserEntity).filter(UserEntity.id == id)
        ) 

        try: 
            async with session.begin(): 
                session.delete(entity) 
            await session.commit() 
            logger.info("User deleted successfully: %s", entity.id)  
            return True
        
        except SQLAlchemyError as e: 
            logger.error("Failed to delete user: %s", e, exc_info=True) 
            await session.rollback()
            return False 
        
        except Exception as e: 
            logger.error("Error: %s", e)
            await session.rollback()
            return False
    
    async def set_email_verification(self,
        session: AsyncSession,
        email: str,
        code: int
        ) -> Optional[bool]:  
        """
        Verificate user for email 

        Args: 
            session (AsyncSession): active SQLAlchemy session  
            email (str): user email 
            code (int): the code that came to the email
        """ 

        entity = await session.execute(
            select(UserEntity).filter(UserEntity.email == email)
        )
        if entity is None: 
            logger.error("User not found: %s", email, exc_info=True)
            raise Exception(f"User with {email} not found") 
        
        try: 
            async with session.begin(): 

                if entity.scalar_one_or_none().code == code: 

                    entity.scalar_one_or_none().isVerify == True 
                    logger.info(f"User {email} verificated")

                    await session.refresh(entity) 
                    await session.commit()  
                    return True
                
                else: 
                    logger.error("Invalid code for verification")

                    await session.rollback() 
                    return False
                                
        except SQLAlchemyError as e: 
            logger.error("Failed verificate user: %s", e, exc_info=True)
            await session.rollback()
            return False
        
        except Exception as e: 
            logger.error("Error: %s", e)
            await session.rollback()
            return False
    @staticmethod
    def _generate_confirmation_code() -> int:
        """Generate random 4-digit code (e.g., for email confirmation)."""
        return random.randint(1000, 9999) 
    

