from pydantic import BaseModel
import uuid

class TripGenerateRequest(BaseModel):
    prompt: str
    user_id: uuid.UUID