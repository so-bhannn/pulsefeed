from fastapi_users import UUIDIDMixin, BaseUserManager

from dotenv import loadenv
import os
import uuid

from app.db import User

SECRET=os.getenv("SECRET_KEY")

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret=SECRET
    verification_token_secret=SECRET