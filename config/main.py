from fastapi import FastAPI
from accounts.router import router as accountsRouter
from book.router import router as booksRouter


from . import settings

app = FastAPI()
app.include_router(accountsRouter)
app.include_router(booksRouter)