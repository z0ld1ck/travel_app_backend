from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.models.collection import Collection
from app.models.trip import Trip
import uuid


class CollectionRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: uuid.UUID, name: str) -> Collection:
        collection = Collection(
            user_id=user_id,
            name=name
        )
        self.db.add(collection)
        await self.db.commit()

        # загружаем заново с relations
        return await self.get_by_id(collection.id)

    async def get_by_id(self, collection_id: uuid.UUID) -> Collection | None:
        result = await self.db.execute(
            select(Collection)
            .options(selectinload(Collection.trips))
            .where(Collection.id == collection_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: uuid.UUID) -> list[Collection]:
        result = await self.db.execute(
            select(Collection)
            .options(selectinload(Collection.trips))
            .where(Collection.user_id == user_id)
            .order_by(Collection.created_at.desc())
        )
        return list(result.scalars().all())

    async def add_trip(
        self,
        collection_id: uuid.UUID,
        trip_id: uuid.UUID
    ) -> Collection | None:
        """
        Добавляем поездку в коллекцию.
        Обновляем collection_id в таблице trips.
        """
        # находим поездку
        trip_result = await self.db.execute(
            select(Trip).where(Trip.id == trip_id)
        )
        trip = trip_result.scalar_one_or_none()

        if not trip:
            return None

        # привязываем к коллекции
        trip.collection_id = collection_id
        await self.db.commit()

        # возвращаем обновлённую коллекцию
        return await self.get_by_id(collection_id)

    async def remove_trip(
        self,
        trip_id: uuid.UUID
    ) -> bool:
        """
        Убираем поездку из коллекции.
        Просто обнуляем collection_id.
        """
        trip_result = await self.db.execute(
            select(Trip).where(Trip.id == trip_id)
        )
        trip = trip_result.scalar_one_or_none()

        if not trip:
            return False

        trip.collection_id = None
        await self.db.commit()
        return True

    async def delete(self, collection_id: uuid.UUID) -> bool:
        """
        Удаляем коллекцию.
        Поездки не удаляются — только отвязываются (collection_id = NULL).
        """
        result = await self.db.execute(
            delete(Collection).where(Collection.id == collection_id)
        )
        await self.db.commit()
        return result.rowcount > 0