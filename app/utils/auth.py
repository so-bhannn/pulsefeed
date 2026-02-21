from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_async_session, User

async def get_user_by_email(email:EmailStr, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.email==email))
    user = result.scalars().first()
    return user