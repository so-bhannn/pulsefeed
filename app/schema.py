from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from dotenv import loadenv
import os


from app.db import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class CreateUser(BaseModel):
    first_name:str
    last_name:str | None=None
    username:str

    email:str
    password:str
    
    is_active:bool