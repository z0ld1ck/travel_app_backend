from pydantic import BaseModel, EmailStr
import uuid

class UserRegister(BaseModel):
    name : str
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class TokenResponse(BaseModel):
    access_token : str
    token_type : str="bearer"
    user_id : uuid.UUID
    name : str


