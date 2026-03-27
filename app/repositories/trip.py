from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.models.trip import Trip, ItineraryDay, Hotel
import uuid


class TripRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, trip_data: dict, user_id: uuid.UUID) -> Trip:
        """
        Создаём поездку из JSON который вернул Claude.
        trip_data — это уже распарсенный dict.
        """
        plan = trip_data.get("trip", {})
        budget = trip_data.get("budget_breakdown", {})

        # создаём основную запись поездки
        trip = Trip(
            user_id=user_id,
            title=plan.get("title", "Моя поездка"),
            destination=plan.get("destination", ""),
            is_multi_city=plan.get("is_multi_city", False),
            cities=plan.get("cities"),
            duration_days=plan.get("duration_days", 0),
            total_budget=plan.get("total_budget", 0),
            currency=plan.get("currency", "USD"),
            raw_plan=trip_data  # сохраняем весь JSON как есть
        )
        self.db.add(trip)
        await self.db.flush()  # flush даёт нам trip.id без commit

        # сохраняем дни маршрута
        for day_data in trip_data.get("itinerary", []):
            day = ItineraryDay(
                trip_id=trip.id,
                day_num=day_data.get("day", 0),
                city=day_data.get("city"),
                title=day_data.get("title", ""),
                activities=day_data.get("activities", [])
            )
            self.db.add(day)

        # сохраняем отели
        for hotel_data in trip_data.get("hotels", []):
            hotel = Hotel(
                trip_id=trip.id,
                city=hotel_data.get("city"),
                name=hotel_data.get("name", ""),
                stars=hotel_data.get("stars"),
                price_per_night=hotel_data.get("price_per_night"),
                area=hotel_data.get("area"),
                booking_url=hotel_data.get("booking_url"),
                pros=hotel_data.get("pros", [])
            )
            self.db.add(hotel)

        await self.db.commit()
        await self.db.refresh(trip)
        return trip

    async def get_by_id(self, trip_id: uuid.UUID) -> Trip | None:
        """
        Получаем поездку со всеми связанными данными.
        selectinload — загружает связанные объекты одним запросом.
        """
        result = await self.db.execute(
            select(Trip)
            .options(
                selectinload(Trip.itinerary_days),
                selectinload(Trip.hotels)
            )
            .where(Trip.id == trip_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: uuid.UUID) -> list[Trip]:
        """
        Получаем все поездки юзера — для истории на Home экране.
        Сортируем по дате — новые сначала.
        """
        result = await self.db.execute(
            select(Trip)
            .where(Trip.user_id == user_id)
            .order_by(Trip.created_at.desc())
        )
        return list(result.scalars().all())

    async def delete(self, trip_id: uuid.UUID) -> bool:
        """
        Удаляем поездку.
        CASCADE в модели удалит itinerary_days и hotels автоматически.
        """
        result = await self.db.execute(
            delete(Trip).where(Trip.id == trip_id)
        )
        await self.db.commit()
        return result.rowcount > 0