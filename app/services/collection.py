import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.collection import CollectionRepository


class CollectionService:

    def __init__(self, db: AsyncSession):
        self.repo = CollectionRepository(db)

    async def create(self, user_id: uuid.UUID, name: str):
        return await self.repo.create(user_id, name)

    async def get_collection(self, collection_id: uuid.UUID):
        collection = await self.repo.get_by_id(collection_id)
        if not collection:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Коллекция не найдена"
            )
        return collection

    async def get_user_collections(self, user_id: uuid.UUID):
        return await self.repo.get_by_user(user_id)

    async def add_trip(self, collection_id: uuid.UUID, trip_id: uuid.UUID):
        collection = await self.repo.add_trip(collection_id, trip_id)
        if not collection:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Поездка не найдена"
            )
        return collection

    async def remove_trip(self, trip_id: uuid.UUID):
        removed = await self.repo.remove_trip(trip_id)
        if not removed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Поездка не найдена"
            )
        return {"message": "Поездка убрана из коллекции"}

    async def delete(self, collection_id: uuid.UUID):
        deleted = await self.repo.delete(collection_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Коллекция не найдена"
            )
        return {"message": "Коллекция удалена"}