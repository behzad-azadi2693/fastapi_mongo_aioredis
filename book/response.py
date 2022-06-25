from pydantic import BaseModel


class BookListResponse(BaseModel):
    name: str
    lang: str
    image: str

    class Config:
        orm_mode = True


class BookResponse(BaseModel):
    name: str
    page: int
    price: float
    isbn11: int
    isbn13: int
    lang: str
    description: str
    image: str
    author: str

    class Config:
        orm_mode = True