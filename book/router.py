from .schema import BookSchema, CommentSchema
from fastapi import Depends, File, UploadFile, Path
from .utils import router, collection
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.settings import BASE_DIR, redis
from .response import BookResponse, BookListResponse
from accounts.utils import get_current_user
from accounts.schema import UserSchema
import os


@router.get('/all/', response_model=list[BookListResponse])
async def all_book():
    books = []
    
    async for book in collection.find():
        books.append(book)

    return books


@router.get('/{name:str}/', response_model=BookResponse)
async def get_book(name:str=Path()):
    book = await collection.find_one({'name':name})

    if book is None:
        return JSONResponse(status_code=400, content='book is not exists')

    return book


@router.post('/create/book/')
async def create_book(book:BookSchema=Depends(),user:UserSchema=Depends(get_current_user)):
    if user.get('admin') == 'false':
        return JSONResponse(status_code=404, content='the url not found')
    
    check_book = await collection.find_one({'name':book.image.filename})
    
    if check_book is not None:
        return JSONResponse(status_code=404, content='book is exists')

    pre, post = book.image.filename.split('.')
    path_save = f"{BASE_DIR}/media/{book.name}.{post}"

    with open(path_save, 'wb') as f:
        image = await book.image.read()
        f.write(image)

    book.image = path_save
    book = jsonable_encoder(book)

    create_book = await collection.insert_one(book, {'image':path_save})
    book = await collection.find_one({'name':book.get('name')})

    return JSONResponse(status_code=200, content=f'{book}')


@router.delete('/delete/book/{name:str}/')
async def delete_book(name:str=Path(), user:UserSchema=Depends(get_current_user)):
    if user.get('admin') == 'false':
        return JSONResponse(status_code=404, content='the url not found')
  
    book = await collection.find_one({'name':name})

    if book:
        os.remove(book.get('image'))
        await collection.delete_one({'name':name})
        return JSONResponse(status_code=200, content='book removed successfully')

    return JSONResponse(status_code=404, content='book is not found')


