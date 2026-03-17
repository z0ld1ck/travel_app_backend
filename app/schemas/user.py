from pydantic import BaseModel, EmailStr
import uuid

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

