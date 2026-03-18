from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.services.claude import ClaudeService
from app.schemas.trip import TripGenerateRequest

router = APIRouter(prefix="/trips", tags=["Trips"])

claude_service = ClaudeService()


@router.post("/generate")
async def generate_trip(data: TripGenerateRequest):
    """
    Принимает промпт от юзера.
    Возвращает SSE поток с планом поездки.
    """

    # если запрос слишком короткий — просим уточнить
    if claude_service.needs_clarification(data.prompt):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Уточни направление и бюджет. Например: хочу в Токио на 7 дней, бюджет $1500"
        )

    # StreamingResponse принимает генератор
    # и отправляет каждый yield сразу клиенту
    return StreamingResponse(
        claude_service.generate_trip_plan(data.prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
