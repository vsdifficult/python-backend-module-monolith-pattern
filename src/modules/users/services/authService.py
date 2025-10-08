from src.modules.users.repository.userRepository import UserRepository
from src.modules.users.dto.userDto import RegisterUserDto, UserDto

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

import logging
import bcrypt
import jwt
from datetime import datetime, timedelta


class AuthResultDto(BaseModel):
    success: bool
    message: str
    error: Optional[str] = None
    token: Optional[str] = None
    user: Optional[UserDto] = None


class AuthService:
    """Authentication Service"""

    def __init__(
        self,
        logger: logging.Logger,
        userRepo: UserRepository,
        jwt_secret: str,
        jwt_algorithm: str = "HS256",
        token_expire_minutes: int = 60
    ):
        self._logger = logger
        self._userRepository = userRepo
        self._jwt_secret = jwt_secret
        self._jwt_algorithm = jwt_algorithm
        self._token_expire_minutes = token_expire_minutes

    async def login(
        self,
        session: AsyncSession,
        email: str,
        password: str
    ) -> AuthResultDto:
        """
        Login user for system

        Args:
            session (AsyncSession)
            email (str)
            password (str)
        """
        try:
            user = await self._userRepository.get_by_email(session, email)

            if not user:
                return AuthResultDto(
                    success=False,
                    message="User not found",
                    error="USER_NOT_FOUND"
                )

            if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
                return AuthResultDto(
                    success=False,
                    message="Invalid credentials",
                    error="INVALID_PASSWORD"
                )

            token = await self._generate_token(user)

            return AuthResultDto(
                success=True,
                message="Login successful",
                token=token,
                user=UserDto.from_orm(user)
            )

        except Exception as e:
            self._logger.error(f"Login failed for user {email}: {e}", exc_info=True)
            return AuthResultDto(
                success=False,
                message="Internal server error",
                error="INTERNAL_ERROR"
            )

    async def signup(
        self,
        session: AsyncSession,
        body: RegisterUserDto
    ) -> AuthResultDto:
        """
        Register user for system

        Args:
            session (AsyncSession)
            body (RegisterUserDto)
        """
        try:
            user = await self._userRepository.create_user(session, body)

            if user is None:
                self._logger.error(f"Register failed for email {body.email}", exc_info=True)
                return AuthResultDto(
                    success=False,
                    message="Register failed",
                    error="USER_CREATION_FAILED"
                )

            token = await self._generate_token(user)

            self._logger.info(f"Register successful for email {user.email}")

            return AuthResultDto(
                success=True,
                message="Register successful",
                token=token,
                user=UserDto.from_orm(user)
            )

        except Exception as e:
            self._logger.error(f"Register failed for email {body.email}: {e}", exc_info=True)
            return AuthResultDto(
                success=False,
                message="Internal server error",
                error="INTERNAL_ERROR"
            )

    async def _generate_token(self, user) -> str:
        """
        Generate JWT token for user (async style, but sync work inside)
        """
        expire = datetime.utcnow() + timedelta(minutes=self._token_expire_minutes)
        token_payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": expire
        }
        token = jwt.encode(token_payload, self._jwt_secret, algorithm=self._jwt_algorithm)
        return token

