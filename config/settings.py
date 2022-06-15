import motor.motor_asyncio
from dotenv import load_dotenv
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR/'.env'))

SECRET_KEY = os.getenv('SECRET_KEY')


engine = os.getenv('DB_ENGINE')

connection = motor.motor_asyncio.AsyncIOMotorClient(engine)

db = connection[os.getenv('DB_NAME')]

try:
    os.mkdir(os.path.join(BASE_DIR, 'media'))
    print('directory for save manage is created')
except:
    print('directory is exits')
