from fastapi import APIRouter
from pydantic import EmailStr
from app.utils.auth import get_user_by_email

router=APIRouter()

@router.get('/users/{email}')
async def get_user(email:EmailStr):
    return get_user_by_email(email=email)