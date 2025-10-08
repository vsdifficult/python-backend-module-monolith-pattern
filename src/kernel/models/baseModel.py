from pydantic import BaseModel 
from datetime import datetime
import uuid 
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): pass