from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class TripGenerateRequest(BaseModel):
    prompt: str
    user_id: uuid.UUID


class TripSaveRequest(BaseModel):
    plan: dict
    user_id: uuid.UUID


class ActivitySchema(BaseModel):
    time: str
    name: str
    description: str
    cost: float
    type: str


class ItineraryDaySchema(BaseModel):
    day_num: int
    city: Optional[str] = None
    title: str
    activities: list[ActivitySchema]


class HotelSchema(BaseModel):
    city: Optional[str] = None
    name: str
    stars: Optional[int] = None
    price_per_night: Optional[float] = None
    area: Optional[str] = None
    booking_url: Optional[str] = None
    pros: Optional[list[str]] = None


class BudgetBreakdown(BaseModel):
    accommodation: float
    food: float
    transport: float
    activities: float
    misc: float


class TripResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    destination: str
    is_multi_city: bool
    cities: Optional[list[str]] = None
    duration_days: int
    total_budget: float
    currency: str
    created_at: datetime
    itinerary_days: list[ItineraryDaySchema] = []
    hotels: list[HotelSchema] = []

    class Config:
        from_attributes = True


class TripListItem(BaseModel):
    id: uuid.UUID
    title: str
    destination: str
    duration_days: int
    total_budget: float
    currency: str
    created_at: datetime

    class Config:
<<<<<<< HEAD
        from_attributes = True
=======
        from_attributes = True                                                                                                                                                                                                                                                                                                                                                                                                              1111111111111111111111111111111111111111111
>>>>>>> ca717af4207e679fe0d962d635aab739324224dc
