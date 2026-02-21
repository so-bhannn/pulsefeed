from pydantic import BaseModel
class CreateUser(BaseModel):
    username:str
    email:str
    password:str
    first_name:str
    last_name:str | None=None

class UserOut(BaseModel):
    id: str
    username: str
    email: str
    first_name : str
    last_name: str | None=None

    class Config:
        from_attributes=True