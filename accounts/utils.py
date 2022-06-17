from config.settings import db, SECRET_KEY, email_conf
from .schema import UserSchema
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema
import jwt




collection = db['Users']

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/accounts/login/')

router = APIRouter(prefix='/accounts', tags=['accounts'])

psw_ctx = CryptContext(schemes='bcrypt', deprecated='auto')


async def get_current_user(token: UserSchema=Depends(oauth2_schema)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    user_current = await collection.find_one({'email':payload.get('email')})

    if user_current is None:
        return HTTPException(status_code=401, detail='user is not found')
    
    return {
        'email':user_current.get('email'),
        'email_check':user_current.get('email_check'),
        'admin':user_current.get('admin')
        }


def sending_token(email_auth):
    data = {"email_auth":email_auth, "exp": datetime.now() + timedelta(hours=5)}
    token = jwt.encode( data, SECRET_KEY, algorithm='HS256')

    '''
    html = f'<a url="{token}">click this link for activate account</a>'

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email_auth,  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )

    fm = FastMail(email_conf)
    await fm.send_message(message)
    '''
    print("token for activate email",token)


def check_time(time):
    if time < datetime.now():
        return False
    
    return True