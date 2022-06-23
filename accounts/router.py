from fastapi import Depends, Form, Path, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from .schema import CreateUserSchema, LoginUserSchema, UserSchema, UpdatePassword
from .response import UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from .utils import collection, psw_ctx, router, get_current_user, sending_token, check_time
from config.settings import SECRET_KEY
import jwt


@router.get('/get/user/{email}/', response_model=UserResponse)
async def get_user(email:EmailStr=Form):#, user:UserSchema=Depends(get_current_user)):


    user_info = await collection.find_one({'email':email})

    if user_info is None:
        return JSONResponse(status_code=400, content='user not exists')

    return user_info


@router.get('/update/user/', response_model=UserResponse)
async def user_update(user_info:UserSchema=Depends(), user:UserSchema=Depends(get_current_user)):
    if user.get('admin') == 'false':
        return JSONResponse(status_code=404, content='the url not found')
    
    data = {'email_check':user_info.email_check, 'admin':user_info.admin}
    user_update = await collection.find_one_and_update({'email':user_info.email},{'$set':data})

    print(user_info.schema_json(indent=2))

    if user_update is None:
        return JSONResponse(status_code=400, content=f'user {user_info.email} not found')

    return user_info


@router.post('/create/user/')
async def create_user(backgroundtasks:BackgroundTasks, user:CreateUserSchema=Depends()):
    user_check = await collection.find_one({'email':user.email})
    if user_check is not None:
        return JSONResponse(status_code=400, content='user is exists')

    passwd_hash = psw_ctx.hash(user.password)
    await collection.insert_one({'email':user.email, 'password':passwd_hash, 'email_check':'false', 'admin':'false'})

    backgroundtasks.add_task(sending_token, user.email)

    return JSONResponse(status_code=201, content=f'user with email {user.email} created')


@router.post('/login/')
async def login(data:OAuth2PasswordRequestForm=Depends()):
    email = data.username
    password = data.password

    user = await collection.find_one({'email':email})

    if user is None:
        return JSONResponse(status_code=400, content='user not found')
    
    if user.get('email_check') == 'false':
        return JSONResponse(status_code=404, content='user is not activate')

    elif not psw_ctx.verify(password , user.get('password')):
        return JSONResponse(status_code=400, content='password not correct')

    user_dict = {
        'email': user.get('email'),
        'password': user.get('password'),
    }

    access_token = jwt.encode(user_dict, SECRET_KEY)

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/send/again/token/')
async def send_again_token(backgroundtasks:BackgroundTasks, email:EmailStr=Form()):
    user = await collection.find_one({'email':email, 'email_check':'false'})

    if user is None:
        return JSONResponse(status_code=404, content='user is not exists please check email field')

    backgroundtasks.add_task(sending_token, email)

    return JSONResponse(status_code=200, content='please check email box and click for activate on email ')    


@router.put('/activator/user/{token:str}')
async def user_activatore(token:str=Path(...)):
    token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    user = await collection.find_one({'email':token.get('email_auth')})

    if user is None and not check_time(token.get('exp')):
        return JSONResponse(status_code=404, content='token is denied please again Re-request token')

    data = {'email_check':'true'}

    await collection.update_one({'email':user.get('email')}, {"$set": data})

    return JSONResponse(status_code=200, content='your account activate please login in site')


@router.put('/update/password/{token:str}')
async def update_password(token:str=Path(),user:UpdatePassword=Depends()):
    token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    email = token.get('email_auth')

    get_user = await collection.find_one({'email':email})

    if get_user is None  and not check_time(token.get('exp')):
        return JSONResponse(status_code=404, content='token is denied please again Re-request token')

    passwd_hash = psw_ctx.hash(user.password)
    await collection.update_one({'email':email, '$set':{'password':passwd_hash}})


    return JSONResponse(status_code=200, content='password is updated please login with new password')

    