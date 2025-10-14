from pydantic import BaseModel 

class NotificationDto(BaseModel): 
    message: str 
    