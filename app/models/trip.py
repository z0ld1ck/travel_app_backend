import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    collection_id = Column(UUID(as_uuid=True), ForeignKey("collections.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(200), nullable=False)
    destination = Column(String(200), nullable=False)
    is_multi_city = Column(Boolean, default=False)
    cities = Column(JSONB, nullable=True)
    duration_days = Column(Integer, nullable=False)
    total_budget = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    raw_plan = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="trips")
    collection = relationship("Collection", back_populates="trips")
    itinerary_days = relationship("ItineraryDay", back_populates="trip", cascade="all, delete")
    hotels = relationship("Hotel", back_populates="trip", cascade="all, delete")


class ItineraryDay(Base):
    __tablename__ = "itinerary_days"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    day_num = Column(Integer, nullable=False)
    city = Column(String(100), nullable=True)
    title = Column(String(200), nullable=False)
    activities = Column(JSONB, nullable=True)

    trip = relationship("Trip", back_populates="itinerary_days")


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    city = Column(String(200), nullable=True)
    name = Column(String(200), nullable=False)
    stars = Column(Integer, nullable=True)
    price_per_night = Column(Numeric(10, 2), nullable=True)
    area = Column(String(200), nullable=True)
    booking_url = Column(Text, nullable=True)
    pros = Column(JSONB, nullable=True)

    trip = relationship("Trip", back_populates="hotels")