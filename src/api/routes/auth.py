from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.kernel.database.database import get_db
from src.kernel.services.dataService import DataService
from src.modules.users.dto.userDto import LoginUserDto, RegisterUserDto, User
import logging

class AuthRouter:
    """Encapsulates all auth routes in a class"""

    def __init__(self, data_service: DataService, logger: logging.Logger = None):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.data_service = data_service
        self.logger = logger or logging.getLogger(__name__)
        self._register_routes()

    def _register_routes(self):
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/signup", self.signup, methods=["POST"])

    async def login(self, body: LoginUserDto, db: AsyncSession = Depends(get_db)):
        """Login user"""
        result = await self.data_service.auth_service.login(db, body)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return {
            "success": result.success,
            "message": result.message,
            "token": result.token,
            "user": result.user
        }

    async def signup(self, body: RegisterUserDto, db: AsyncSession = Depends(get_db)):
        """Register user"""
        result = await self.data_service.auth_service.signup(db, body)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return {
            "success": result.success,
            "message": result.message,
            "token": result.token,
            "user": result.user
        }
