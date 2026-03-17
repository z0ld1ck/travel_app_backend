from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class UserRepository:

<<<<<<< HEAD
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
=======
    def __init__(self, db:AsyncSession):
        self.db=db

    async def get_my_email(self, email: str)->User | None:
        result= await self.db.execute(
            select(User).where(User.email==email)
        )
        return result.scalar_one_or_none()
    
    async def create(self, name: str, email: str, password_hash: str)->User:
        user=User(
>>>>>>> 37b5bafc8839473980d31976cb119392abc83d47
            name=name,
            email=email,
            password_hash=password_hash
        )
<<<<<<< HEAD
        self.db.add(user)          # добавляем в сессию
        await self.db.commit()     # сохраняем в БД
        await self.db.refresh(user) # обновляем объект из БД (чтобы получить id и created_at)
=======
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
>>>>>>> 37b5bafc8839473980d31976cb119392abc83d47
        return user