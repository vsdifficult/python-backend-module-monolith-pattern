from src.modules.users.repository.userRepository import UserRepository
from src.modules.users.dto.userDto import RegisterUserDto, UserDto, LoginUserDto, User, UserWithPassword

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

import logging
import bcrypt
import jwt
from datetime import datetime, timedelta
import random


class AuthResultDto(BaseModel):
    success: bool
    message: str
    error: Optional[str] = None
    token: Optional[str] = None
    user: Optional[User] = None


class AuthService:
    """Authentication Service"""

    def __init__(
        self,
        logger: logging.Logger,
        userRepo: UserRepository,
        jwt_secret: str,
        jwt_algorithm: str = "HS256",
        token_expire_minutes: int = 60,
    ):
        self._logger = logger
        self._userRepository = userRepo
        self._jwt_secret = jwt_secret
        self._jwt_algorithm = jwt_algorithm
        self._token_expire_minutes = token_expire_minutes

    async def login(self, session: AsyncSession, body: LoginUserDto) -> AuthResultDto:
        """
        Login user for system

        Args:
            session (AsyncSession)
            body (LoginUserDto)
        """
        try:
            user = await self._userRepository.get_by_email(session, body.email)

            if not user:
                return AuthResultDto(
                    success=False,
                    message="User not found",
                    error="USER_NOT_FOUND",
                )

            if not bcrypt.checkpw(
                body.password.encode("utf-8"), user.password.encode("utf-8")
            ):
                return AuthResultDto(
                    success=False,
                    message="Invalid credentials",
                    error="INVALID_PASSWORD",
                )

            token = await self._generate_token(user)

            return AuthResultDto(
                success=True,
                message="Login successful",
                token=token,
                user=User.from_orm(user),
            )

        except Exception as e:
            self._logger.error(f"Login failed for user {body.email}: {e}", exc_info=True)
            return AuthResultDto(
                success=False,
                message="Internal server error",
                error="INTERNAL_ERROR",
            )

    async def signup(self, session: AsyncSession, body: RegisterUserDto) -> AuthResultDto:
        """
        Register user for system

        Args:
            session (AsyncSession)
            body (RegisterUserDto)
        """
        try:
            hashed_password = bcrypt.hashpw(
                body.password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            user_with_password = UserWithPassword(
                **body.dict(),
                password=hashed_password,
            )

            user_id = await self._userRepository.create_user(session, user_with_password)

            if user_id is None:
                self._logger.error(
                    f"Register failed for email {body.email}", exc_info=True
                )
                return AuthResultDto(
                    success=False,
                    message="Register failed",
                    error="USER_CREATION_FAILED",
                )

            user = await self._userRepository.get_by_id(session, user_id)

            token = await self._generate_token(user)

            self._logger.info(f"Register successful for email {user.email}")

            return AuthResultDto(
                success=True,
                message="Register successful",
                token=token,
                user=User.from_orm(user),
            )

        except Exception as e:
            self._logger.error(
                f"Register failed for email {body.email}: {e}", exc_info=True
            )
            return AuthResultDto(
                success=False,
                message="Internal server error",
                error="INTERNAL_ERROR",
            )

    async def verify_email(self, session: AsyncSession, email: str, code: int) -> bool:
        """
        Verify user email

        Args:
            session (AsyncSession)
            email (str)
            code (int)
        """
        return await self._userRepository.set_email_verification(session, email, code)

    async def _generate_token(self, user) -> str:
        """
        Generate JWT token for user (async style, but sync work inside)
        """
        expire = datetime.utcnow() + timedelta(minutes=self._token_expire_minutes)
        token_payload = {"sub": str(user.id), "email": user.email, "exp": expire}
        token = jwt.encode(token_payload, self._jwt_secret, algorithm=self._jwt_algorithm)
        return token

    @staticmethod
    def _generate_confirmation_code() -> int:
        """Generate random 4-digit code (e.g., for email confirmation)."""
        return random.randint(1000, 9999)
