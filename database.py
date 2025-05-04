import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from fastapi import Depends
from contextlib import asynccontextmanager

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": True}
)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session