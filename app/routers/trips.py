from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.database import get_db
from app.services.claude import ClaudeService
from app.services.trip import TripService
from app.schemas.trip import (
    TripGenerateRequest,
    TripSaveRequest,
    TripResponse,
    TripListItem
)

router = APIRouter(prefix="/trips", tags=["Trips"])
claude_service = ClaudeService()


@router.post("/generate")
async def generate_trip(data: TripGenerateRequest):
    """
    Генерирует план через Claude.
    Возвращает SSE поток.
    Клиент сам решает сохранять или нет.
    """
    if claude_service.needs_clarification(data.prompt):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Уточни направление и бюджет. Например: хочу в Токио на 7 дней, бюджет $1500"
        )

    return StreamingResponse(
        claude_service.generate_trip_plan(data.prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/save", response_model=TripResponse)
async def save_trip(
    data: TripSaveRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Сохраняет готовый план в БД.
    Flutter вызывает этот эндпоинт после получения done события.
    """
    service = TripService(db)
    return await service.save_trip(data.plan, data.user_id)


@router.get("/history/{user_id}", response_model=list[TripListItem])
async def get_history(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    История всех поездок юзера.
    Используется на Home экране.
    """
    service = TripService(db)
    return await service.get_user_trips(user_id)


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(
    trip_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить поездку по id.
    Используется когда юзер открывает план из истории.
    """
    service = TripService(db)
    return await service.get_trip(trip_id)


@router.delete("/{trip_id}")
async def delete_trip(
    trip_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить поездку из истории.
    """
    service = TripService(db)
    return await service.delete_trip(trip_id)