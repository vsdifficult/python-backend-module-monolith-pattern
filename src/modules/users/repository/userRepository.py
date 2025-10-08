
from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4

import logging

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.modules.users.entities.userEntity import UserEntity
from src.modules.users.dto.userDto import RegisterUserDto, UserWithPassword

logger = logging.getLogger(__name__)

class UserRepository:
    """Repository for working with UserEntity."""

    async def create_user(
        self, session: AsyncSession, user: UserWithPassword
    ) -> Optional[UUID]:
        """
        Create new user in database.

        Args:
            session (AsyncSession): active SQLAlchemy session
            user (UserWithPassword): DTO with user data

        Returns:
            UUID | None: User id if created successfully, otherwise None
        """
        entity = UserEntity(
            id=uuid4(),
            email=user.email,
            name=user.name,
            password=user.password,
            role=user.role,
            code=user.code,
        )

        try:
            session.add(entity)
            await session.flush()
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

    async def get_by_id(self, session: AsyncSession, id: UUID) -> Optional[UserEntity]:
        """Find user by id."""
        result = await session.execute(
            select(UserEntity).filter(UserEntity.id == id)
        )
        return result.scalar_one_or_none()

    async def delete_user(self, session: AsyncSession, id: UUID) -> bool:
        """
        Delete user

        Args:
            session (AsyncSession): active SQLAlchemy session
            id (UUID): user id

        Returns:
            True | False: True if deleted successfully, otherwise False
        """
        entity = await session.get(UserEntity, id)

        if entity is None:
            return False

        try:
            await session.delete(entity)
            await session.flush()
            logger.info("User deleted successfully: %s", id)
            return True
        except SQLAlchemyError as e:
            logger.error("Failed to delete user: %s", e, exc_info=True)
            await session.rollback()
            return False

    async def set_email_verification(self, session: AsyncSession, email: str, code: int) -> bool:
        """
        Verify user by email and code

        Args:
            session (AsyncSession): active SQLAlchemy session
            email (str): user email
            code (int): the code that came to the email
        """
        user = await self.get_by_email(session, email)
        if user is None or user.code != code:
            return False

        try:
            user.is_verify = True
            await session.flush()
            logger.info(f"User {email} verified")
            return True
        except SQLAlchemyError as e:
            logger.error("Failed to verify user: %s", e, exc_info=True)
            await session.rollback()
            return False

    async def update_user(self, session: AsyncSession, id: UUID, data: dict) -> Optional[UserEntity]:
        """
        Update user data

        Args:
            session (AsyncSession): active SQLAlchemy session
            id (UUID): user id
            data (dict): data to update

        Returns:
            UserEntity | None: updated user entity or None
        """
        try:
            await session.execute(update(UserEntity).where(UserEntity.id == id).values(**data))
            await session.flush()
            return await session.get(UserEntity, id)
        except SQLAlchemyError as e:
            logger.error("Failed to update user: %s", e, exc_info=True)
            await session.rollback()
            return None
