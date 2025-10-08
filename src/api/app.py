from fastapi import FastAPI
from src.kernel.services.dataService import DataService
from src.kernel.database.config import settings
from .routes.users import UserRouter
from .routes.auth import AuthRouter
import logging

logger = logging.getLogger(__name__)
data_service = DataService(jwt_secret=settings.jwt_secret, logger=logger)

user_router = UserRouter(data_service=data_service)
auth_router = AuthRouter(data_service=data_service)

app = FastAPI(
    title="Python Backend API",
    description="A FastAPI backend application with user management and other modules.",
    version="1.0.0",
    contact={
        "name": "Developer",
        "email": "developer@example.com",
    },
    license_info={
        "name": "MIT",
    },
)
app.include_router(auth_router.router)
app.include_router(user_router.router)

