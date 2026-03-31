from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class CollectionCreate(BaseModel):
    user_id: uuid.UUID
    name: str


class TripInCollection(BaseModel):
    id: uuid.UUID
    title: str
    destination: str
    duration_days: int
    total_budget: float
    currency: str
    created_at: datetime

    class Config:
        from_attributes = True


class CollectionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    created_at: datetime
    trips: list[TripInCollection] = []

    class Config:
        from_attributes = True


class AddTripRequest(BaseModel):
    trip_id: uuid.UUID