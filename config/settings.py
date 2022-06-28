import motor.motor_asyncio
from dotenv import load_dotenv
import os
from pathlib import Path
from fastapi_mail import ConnectionConfig
import aioredis


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR/'.env'))

SECRET_KEY = os.getenv('SECRET_KEY')


engine = os.getenv('DB_ENGINE')

connection = motor.motor_asyncio.AsyncIOMotorClient(engine)

db = connection[os.getenv('DB_NAME')]

redis = aioredis.from_url(
        os.getenv('REDIS_ENGINE'), db=1,password=os.getenv('REDIS_PASSWORD'), decode_responses=True
    )

email_conf =''' ConnectionConfig(
        MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
        MAIL_FROM = os.getenv('MAIL_FROM'),
        MAIL_PORT = os.getenv('MAIL_PORT'),
        MAIL_SERVER = os.getenv('MAIL_SERVER'),
        MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME'),
        MAIL_TLS = True,
        MAIL_SSL = False,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )
'''

try:
    os.mkdir(os.path.join(BASE_DIR, 'media'))
    print('directory for save manage is created')
except:
    print('directory is exits')
