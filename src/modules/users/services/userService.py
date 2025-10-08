from src.modules.users.repository.userRepository import UserRepository
from src.modules.users.dto.userDto import UserDto
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
import logging

class UserService:
    """User Service"""

    def __init__(self, logger: logging.Logger, user_repo: UserRepository):
        self._logger = logger
        self._user_repo = user_repo

    async def get_user_by_id(self, session: AsyncSession, user_id: UUID) -> Optional[UserDto]:
        """Get user by id"""
        user = await self._user_repo.get_by_id(session, user_id)
        if user:
            return UserDto.from_orm(user)
        return None

    async def update_user(
        self, session: AsyncSession, user_id: UUID, data: dict
    ) -> Optional[UserDto]:
        """Update user"""
        user = await self._user_repo.update_user(session, user_id, data)
        if user:
            return UserDto.from_orm(user)
        return None

    async def delete_user(self, session: AsyncSession, user_id: UUID) -> bool:
        """Delete user"""
        return await self._user_repo.delete_user(session, user_id)
