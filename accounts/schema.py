from fastapi import Body
from pydantic import BaseModel, validator, EmailStr


class UpdatePassword(BaseModel):
    password:str = Body(..., min_length=8, regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
    confierm_password:str = Body(...,  min_length=8, regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')

    @validator('confierm_password')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise HTTPException(status_code=400, detail='password do not match')
        return v


class CreateUserSchema(BaseModel):
    email:EmailStr = Body(...) 
    password:str = Body(..., min_length=8, regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
    confierm_password:str = Body(...,  min_length=8, regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')

    @validator('confierm_password')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise HTTPException(status_code=400, detail='password do not match')
        return v


class LoginUserSchema(BaseModel):
    email:str
    password:str


class UserSchema(BaseModel):
    email:str
    email_check:str
    admin:str