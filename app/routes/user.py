from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.schema import UserOut
from app.utils.auth import get_user_by_email

router=APIRouter()

@router.get('/users/{email}', response_model=UserOut)
async def get_user(email:EmailStr, session:AsyncSession=Depends(get_async_session)):
    user= await get_user_by_email(email=email,session=session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)