from pydantic import BaseModel, field_serializer
from uuid import UUID
class CreateUser(BaseModel):
    username:str
    email:str
    password:str
    first_name:str
    last_name:str | None=None

class UserOut(BaseModel):
    id: UUID
    username: str
    email: str
    first_name : str
    last_name: str | None=None

    class Config:
        from_attributes=True

    @field_serializer('id')
    def serialize_id(self, value:UUID)->str:
        return str(value)