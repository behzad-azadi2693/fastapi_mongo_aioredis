from fastapi import APIRouter
from config.settings import db

router = APIRouter(prefix='/book', tags=['book'])

collection = db['Books']