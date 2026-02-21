from sqlalchemy import select
from app.db import User

async def get_user_by_email(email, session):
    result = await session.execute(select(User).where(User.email==email))
    user = result.scalars().first()
    return user

async def create_user(details, session):
    