
from src.modules.users.repository.userRepository import UserRepository
from src.modules.users.repository.chatRepository import ChatRepository
from src.modules.users.services.authService import AuthService
from src.modules.users.services.userService import UserService
from src.modules.users.utils.validateUsers import UserValidationService
import logging

class DataService:
    """
    Kernel data service: provides access to all domain services
    via abstraction.
    """

    def __init__(self, jwt_secret: str, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        # Repositories
        self.user_repository = UserRepository()
        self.chat_repository = ChatRepository()

        # Services
        self.user_validation_service = UserValidationService(user_repo=self.user_repository)
        self.auth_service = AuthService(
            logger=self.logger,
            userRepo=self.user_repository,
            jwt_secret=jwt_secret
        )
        self.user_service = UserService(
            logger=self.logger,
            user_repo=self.user_repository,
            chat_repo=self.chat_repository
        )
