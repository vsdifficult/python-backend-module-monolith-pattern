from fastapi import FastAPI
from src.kernel.services.dataService import DataService
from .routes.users import UserRouter
import logging

logger = logging.getLogger(__name__)
data_service = DataService(jwt_secret="", logger=logger)

user_router = UserRouter(data_service=data_service)

app = FastAPI()
app.include_router(user_router.router)