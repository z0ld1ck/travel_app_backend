from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.config import settings

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self,db: AsyncSession):
        self.repo=UserRepository(db)
    
    def _hash_password(self, password: str)->str:
        return pwd_context.hash(password)

    def _verify_password(self, plain: str,hashed:str)->bool:
        return pwd_context.verify(plain,hashed)

    def _crete_token(self,user_id:str)->str:
        expire=datetime.utcnow()+timedelta(days=30)
        payload={
            "sub":user_id,
            "exp":expire
        }
        return jwt.encode(payload,settings.secret_key, algorithm="HS256")

async def register(self,data:UserRegister)->TokenResponse:
    existing=await self.repo.get_by_email(data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже используется"
        )

    password_hash=self._hash_password(data.password)
    user=await self.repo.create(data.name,data.email,password_hash)

    token=self._crete_token(str(user.id))
    return  TokenResponse(
        access_token=token,
        user_id=user.id,
        name=user.name
    )

async def login(self,data:UserLogin)->TokenResponse:
    user=await self.repo.get_by_email(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    if not self._verify_password(data.password,user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    token=self._crete_token(str(user.id))
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        name=user.name
    )