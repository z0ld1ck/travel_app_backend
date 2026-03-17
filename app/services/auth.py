from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.config import settings

# настраиваем bcrypt для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    def _hash_password(self, password: str) -> str:
        # превращаем пароль в хэш
        # "mypassword" → "$2b$12$..."
        return pwd_context.hash(password)

    def _verify_password(self, plain: str, hashed: str) -> bool:
        # сравниваем введённый пароль с хэшем
        # не расшифровывает — просто сравнивает
        return pwd_context.verify(plain, hashed)

    def _create_token(self, user_id: str) -> str:
        # создаём JWT токен
        expire = datetime.utcnow() + timedelta(days=30)
        payload = {
            "sub": user_id,      # subject — id юзера
            "exp": expire        # когда токен истекает
        }
        return jwt.encode(payload, settings.secret_key, algorithm="HS256")

    async def register(self, data: UserRegister) -> TokenResponse:
        # проверяем что email не занят
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже используется"
            )

        # хэшируем пароль и создаём юзера
        password_hash = self._hash_password(data.password)
        user = await self.repo.create(data.name, data.email, password_hash)

        # выдаём токен
        token = self._create_token(str(user.id))
        return TokenResponse(
            access_token=token,
            user_id=user.id,
            name=user.name
        )

    async def login(self, data: UserLogin) -> TokenResponse:
        # ищем юзера по email
        user = await self.repo.get_by_email(data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )

        # проверяем пароль
        if not self._verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )

        # выдаём токен
        token = self._create_token(str(user.id))
        return TokenResponse(
            access_token=token,
            user_id=user.id,
            name=user.name
        )
