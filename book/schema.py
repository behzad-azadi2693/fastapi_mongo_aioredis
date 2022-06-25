from pydantic import BaseModel, validator
from fastapi import Body
from fastapi import File, UploadFile, HTTPException

class BookSchema(BaseModel):
    name: str
    page: int
    price: float
    isbn11: int = Body(...,eq=11)
    isbn13: int = Body(...,eq=13)
    lang: str
    description: str
    image: UploadFile = File()
    author: str

    @validator('image')
    def check_image(cls, v, **kwargs):
        if not v.content_type in ['image/png', 'image/jpg', 'image/jpeg']:
            return HTTPException(status_code=400, detail='filds must be image')
        return v


class CommentSchema(BaseModel):
    name: str
    message: str