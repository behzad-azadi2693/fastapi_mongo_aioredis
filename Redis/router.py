from fastapi import APIRouter, Depends, Path
from config.settings import redis
from accounts.schema import UserSchema
from accounts.utils import get_current_user
from book.response import BookListResponse
from book.utils import collection


router = APIRouter(prefix='/redis', tags=['redis'])


@router.get('/get/my/favroite/', response_model=list[BookListResponse])
async def get_favroite_book(user:UserSchema=Depends(get_current_user)):
    key = f"favorite:{user.get('email')}"
    values = await redis.smembers(key)
    list_favotite = jsonable_encoder(values)

    books = []
    async for book in collection.find({'name':{'$in': list_favotite}}):
        books.append(book)

    return books


@router.post('/add/favroite/book/{book_name:str}/')
async def add_favroite_book(book_name:str = Path(), user:UserSchema=Depends(get_current_user)):
    book = await collection.find_one({'name':book_name})

    if book is None:
        return JSONResponse(status_code=404, content='book is not exists')

    key = f"favorite:{user.get('email')}"
    value = book.get('name')
    await redis.sadd(key, value)
    k = await redis.smembers(key)
    return JSONResponse(status_code=200, content=jsonable_encoder(k))


@router.delete('/delete/book/favroite/{book_name:str}/')
async def delete_favroite_book(book_name:str = Path(), user:UserSchema=Depends(get_current_user)):
    key = f"favorite:{user.get('email')}"
    value = book_name

    answer = await redis.srem(key, value)

    if answer == 0:
        return JSONResponse(status_code=404, content='book is not found')
        
    return JSONResponse(status_code=200, content='book deleted')