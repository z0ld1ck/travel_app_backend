from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.claude import ClaudeService
from app.schemas.trip import TripGenerateRequest, ClarificationResponse

router = APIRouter(prefix="/trips", tags=["Trips"])

claude_service = ClaudeService()

@router.post("/generate")
async def generate_trip(
    data: TripGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Генерирует план поездки через Claude.
    Возвращает SSE поток — клиент получает данные в реальном времени.
    """

    # проверяем нужно ли уточнение
    if claude_service.needs_clarification(data.prompt):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="clarification_needed"
        )

    # возвращаем StreamingResponse — это и есть SSE
    return StreamingResponse(
        claude_service.generate_trip_plan(data.prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"  # отключаем буферизацию nginx
        }
    )