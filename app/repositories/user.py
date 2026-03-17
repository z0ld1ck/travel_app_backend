from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class UserRepository:

    def __init__(self, db:AsyncSession):
        self.db=db

    async def get_my_email(self, email: str)->User | None:
        result= await self.db.execute(
            select(User).where(User.email==email)
        )
        return result.scalar_one_or_none()
    
    async def create(self, name: str, email: str, password_hash: str)->User:
        user=User(
            name=name,
            email=email,
            password_hash=password_hash
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user