from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.kernel.database.database import get_db
from src.kernel.services.dataService import DataService
from src.modules.users.dto.userDto import UserDto
from uuid import UUID
import logging

class UserRouter:
    """Encapsulates all user routes in a class"""

    def __init__(self, data_service: DataService, logger: logging.Logger = None):
        self.router = APIRouter(prefix="/users", tags=["users"])
        self.data_service = data_service
        self.logger = logger or logging.getLogger(__name__)
        self._register_routes()

    def _register_routes(self):
        self.router.add_api_route("/{user_id}", self.get_user, methods=["GET"], response_model=UserDto)
        self.router.add_api_route("/{user_id}", self.update_user, methods=["PUT"], response_model=UserDto)
        self.router.add_api_route("/{user_id}", self.delete_user, methods=["DELETE"])

    async def get_user(self, user_id: UUID, db: AsyncSession = Depends(get_db)):
        """Get user by ID"""
        user = await self.data_service.user_service.get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update_user(self, user_id: UUID, data: dict, db: AsyncSession = Depends(get_db)):
        """Update user"""
        user = await self.data_service.user_service.update_user(db, user_id, data)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def delete_user(self, user_id: UUID, db: AsyncSession = Depends(get_db)):
        """Delete user"""
        if not await self.data_service.user_service.delete_user(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
