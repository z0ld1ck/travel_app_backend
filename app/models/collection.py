import uuid
from sqlalchemy import Column,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Collection(Base):
      __tablename__ = "collections"

      id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
      user_id=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
      name=Column(String(100),nullable=False)
      description=Column(String(255),nullable=True)
      created_at=Column(DateTime(timezone=True),server_default=func.now())
      
      user=relationship("User",back_populates="collections")
      trips= relationship("Trip",back_populates="collection",cascade="all,delete")

      