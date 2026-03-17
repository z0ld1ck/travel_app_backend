from pydantic import BaseModel
import uuid

# Что принимаем при генерации плана
class TripGenerateRequest(BaseModel):
    prompt: str
    user_id: uuid.UUID

# Ответ если нужно уточнение
class ClarificationResponse(BaseModel):
    message: str
    suggestions: list[str]