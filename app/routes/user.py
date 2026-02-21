from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.db import get_async_session, User
from app.schema import CreateUser,UserOut
from app.utils.password import hash_password

router=APIRouter()

@router.get('/users/{email}', response_model=UserOut)
async def get_user_endpoint(email:EmailStr, session:AsyncSession=Depends(get_async_session)):
    try:
        result = await session.execute(select(User).where(User.email==email))
        user=result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data=UserOut.model_validate(user)
        user_data.id = str(user.id)
        return user_data

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.post('/users/', response_model=UserOut)
async def create_user_endpoint(details:CreateUser, session:AsyncSession=Depends(get_async_session)):
    payload=details.model_dump()
    hashed_password=hash_password(payload.pop('password'))
    user = User(**payload, hashed_password=hashed_password)

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return UserOut.model_validate(user)
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")