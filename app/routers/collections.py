from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.database import get_db
from app.services.collection import CollectionService
from app.schemas.collection import (
    CollectionCreate,
    CollectionResponse,
    AddTripRequest
)

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.post("", response_model=CollectionResponse)
async def create_collection(
    data: CollectionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новую коллекцию"""
    service = CollectionService(db)
    return await service.create(data.user_id, data.name)


@router.get("/user/{user_id}", response_model=list[CollectionResponse])
async def get_user_collections(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Все коллекции юзера"""
    service = CollectionService(db)
    return await service.get_user_collections(user_id)


@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(
    collection_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Получить коллекцию по id"""
    service = CollectionService(db)
    return await service.get_collection(collection_id)


@router.post("/{collection_id}/trips", response_model=CollectionResponse)
async def add_trip_to_collection(
    collection_id: uuid.UUID,
    data: AddTripRequest,
    db: AsyncSession = Depends(get_db)
):
    """Добавить поездку в коллекцию"""
    service = CollectionService(db)
    return await service.add_trip(collection_id, data.trip_id)


@router.delete("/{collection_id}/trips/{trip_id}")
async def remove_trip_from_collection(
    collection_id: uuid.UUID,
    trip_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Убрать поездку из коллекции"""
    service = CollectionService(db)
    return await service.remove_trip(trip_id)


@router.delete("/{collection_id}")
async def delete_collection(
    collection_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Удалить коллекцию"""
    service = CollectionService(db)
    return await service.delete(collection_id)