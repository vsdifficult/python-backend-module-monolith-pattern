from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import URL, text 
from .config import settings 

engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = True, 
    pool_size = 5,
    max_overflow = 10
) 
Base = declarative_base() 

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False) 

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session 

    
async def init_db(): 
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)