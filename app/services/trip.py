import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.trip import TripRepository
from app.models.trip import Trip


class TripService:

    def __init__(self, db: AsyncSession):
        self.repo = TripRepository(db)

    async def save_trip(self, plan: dict, user_id: uuid.UUID) -> Trip:
        """
        Сохраняем готовый план в БД.
        plan — это dict который пришёл от Claude.
        """
        try:
            return await self.repo.create(plan, user_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка сохранения плана: {str(e)}"
            )

    async def get_trip(self, trip_id: uuid.UUID) -> Trip:
        """
        Получаем поездку по id.
        Если не найдена — возвращаем 404.
        """
        trip = await self.repo.get_by_id(trip_id)
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Поездка не найдена"
            )
        return trip

    async def get_user_trips(self, user_id: uuid.UUID) -> list[Trip]:
        """
        Получаем историю поездок юзера для Home экрана.
        """
        return await self.repo.get_by_user(user_id)

    async def delete_trip(self, trip_id: uuid.UUID) -> dict:
        """
        Удаляем поездку.
        """
        deleted = await self.repo.delete(trip_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Поездка не найдена"
            )
        return {"message": "Поездка удалена"}