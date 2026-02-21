from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable
from collections.abc import AsyncGenerator
from enum import StrEnum
import uuid
from typing import Optional
from sqlalchemy import Text, String, DateTime, ForeignKey, UUID, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio  import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from datetime import datetime,timezone


DATABASE_URL="sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__="users"

    id: Mapped[uuid.UUID]=mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str]=mapped_column(String,nullable=False)
    email:Mapped[str]=mapped_column(String,nullable=False)
    hashed_password:Mapped[str]=mapped_column(String, nullable=False)

    first_name: Mapped[str]=mapped_column(String, nullable=False)
    last_name: Mapped[Optional[str]]=mapped_column(String)

    is_active:Mapped[Optional[bool]]=mapped_column(Boolean, default=True)

class FileCategory(StrEnum):
    IMAGE="image"
    VIDEO="video"

class Post(Base):
    __tablename__="posts"

    id: Mapped[uuid.UUID] =mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID]=mapped_column(UUID, ForeignKey("users.id"), nullable=False)

    caption: Mapped[Optional[str]]=mapped_column(Text)
    url: Mapped[str]=mapped_column(Text, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_type: Mapped[FileCategory] = mapped_column(
        Enum(FileCategory,native_enum=False),
        default=FileCategory.IMAGE
    )
    created_at:Mapped[DateTime]=mapped_column(
        DateTime,
        default=lambda:datetime.now(timezone.utc)
        )
    
    user:Mapped["User"]=relationship(back_populates="posts")

engine=create_async_engine(DATABASE_URL)
async_sessionmaker=async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=True
    )

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession,None]:
    async with async_sessionmaker() as session:
        yield session

async def get_user_db(session:AsyncGenerator=Depends(get_async_session)):
    yield SQLAlchemyBaseUserTable(session, User)