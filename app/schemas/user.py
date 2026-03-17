from pydantic import BaseModel, EmailStr
import uuid

<<<<<<< HEAD
# Что принимаем при регистрации
class UserRegister(BaseModel):
    name: str
    email: EmailStr  # автоматически валидирует формат email
    password: str

# Что принимаем при логине
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Что отдаём после успешного логина
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: uuid.UUID
    name: str
=======
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


>>>>>>> 37b5bafc8839473980d31976cb119392abc83d47
