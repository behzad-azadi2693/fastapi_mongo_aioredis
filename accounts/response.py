from pydantic import BaseModel
from bson.objectid import ObjectId


class UserResponse(BaseModel):
    _id:ObjectId()
    email:str
    email_check:str
    admin:bool

    class Config:
        orm_mode = True