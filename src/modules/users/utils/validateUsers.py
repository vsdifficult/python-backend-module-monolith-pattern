from src.modules.users.repository.userRepository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.users.dto.userDto import RegisterUserDto

from pydantic import EmailStr
import re


class UserValidationService:
    """
    User validation service:
    - email format
    - password strength
    - uniqueness
    """

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def validate_email_unique(self, session: AsyncSession, email: str) -> bool:
        """Check if the email is unique"""
        user = await self._user_repo.get_by_email(session, email)
        return user is None

    def validate_email_format(self, email: str) -> bool:
        """Simple email format check"""
        try:
            EmailStr.validate(email)
            return True
        except ValueError:
            return False

    def validate_password_strength(self, password: str) -> bool:
        """
        Check password strength:
        - minimum 8 characters
        - at least one uppercase letter
        - at least one digit
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        return True

    async def validate_register(self, session: AsyncSession, dto: RegisterUserDto) -> list[str]:
        """Check all conditions for registration"""
        errors = []

        if not self.validate_email_format(dto.email):
            errors.append("Invalid email format")

        if not self.validate_password_strength(dto.password):
            errors.append("Weak password")

        if not await self.validate_email_unique(session, dto.email):
            errors.append("Email already in use")

        return errors
