from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.kernel.database.database import get_db
from src.kernel.services.dataService import DataService
from src.modules.users.dto.userDto import UserDto
from uuid import UUID
import logging

router = APIRouter(prefix="/users", tags=["users"])

logger = logging.getLogger(__name__)

dataService = DataService(jwt_secret="", logger=logger)  

@router.get("/{user_id}", response_model=UserDto)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get user by id"""
    user = await dataService.user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserDto)
async def update_user(user_id: UUID, data: dict, db: AsyncSession = Depends(get_db)):
    """Update user"""
    user = await dataService.user_service.update_user(db, user_id, data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete user"""
    if not await dataService.user_service.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
