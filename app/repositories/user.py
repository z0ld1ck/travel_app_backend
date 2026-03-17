from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class UserRepository:

    def __init__(self, db: AsyncSession):
        # получаем сессию БД через dependency injection
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        # ищем юзера по email
        # select(User) = "SELECT * FROM users"
        # where = "WHERE email = ?"
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, name: str, email: str, password_hash: str) -> User:
        # создаём нового юзера
        user = User(
            name=name,
            email=email,
            password_hash=password_hash
        )
        self.db.add(user)          # добавляем в сессию
        await self.db.commit()     # сохраняем в БД
        await self.db.refresh(user) # обновляем объект из БД (чтобы получить id и created_at)
        return user