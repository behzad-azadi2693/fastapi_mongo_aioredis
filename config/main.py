from fastapi import FastAPI
from accounts.router import router as accountsRouter


from . import settings

app = FastAPI()
app.include_router(accountsRouter)