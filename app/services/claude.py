import json
import anthropic
from app.config import settings

SYSTEM_PROMPT = """You are an expert travel planner.
When given a destination, duration, budget and interests —
respond ONLY with a valid JSON object, no other text, no markdown.

Use this exact schema:
{
  "trip": {
    "title": "string",
    "destination": "string",
    "duration_days": number,
    "total_budget": number,
    "currency": "string",
    "is_multi_city": boolean,
    "cities": ["city1", "city2"] or null
  },
  "itinerary": [
    {
      "day": number,
      "city": "string or null",
      "title": "string",
      "activities": [
        {
          "time": "09:00",
          "name": "string",
          "description": "string",
          "cost": number,
          "type": "food|culture|nature|transport|accommodation"
        }
      ]
    }
  ],
  "hotels": [
    {
      "city": "string or null",
      "name": "string",
      "stars": number,
      "price_per_night": number,
      "area": "string",
      "booking_url": "https://www.booking.com/searchresults.html?ss=CITYNAME",
      "pros": ["string"]
    }
  ],
  "budget_breakdown": {
    "accommodation": number,
    "food": number,
    "transport": number,
    "activities": number,
    "misc": number
  }
}

IMPORTANT:
- All costs must fit within the user's total budget
- booking_url must be real Booking.com search URL for that city
- For multi-city trips fill city field in itinerary and hotels
- Respond ONLY with JSON, no markdown, no explanation
- Use the same currency as specified by user"""


class ClaudeService:

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def generate_trip_plan(self, prompt: str):
        """
        Генератор — отдаёт SSE события по одному.
        Каждый yield немедленно уходит клиенту.
        """

        # статус 1 — пользователь видит что происходит
        yield self._status("Анализирую направление...")

        full_text = ""

        try:
            # открываем стриминг с Claude
            # with ... as stream — соединение открыто пока внутри блока
            with self.client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:

                yield self._status("Строю маршрут...")

                # читаем ответ по кускам
                for chunk in stream.text_stream:
                    full_text += chunk
                    yield self._chunk(chunk)

            yield self._status("Финализирую план...")

            # парсим финальный JSON
            trip_data = json.loads(full_text)

            # отправляем готовый план
            yield self._done(trip_data)

        except json.JSONDecodeError:
            yield self._error("Не удалось распарсить план. Попробуй снова.")
        except Exception as e:
            yield self._error(str(e))

    def needs_clarification(self, prompt: str) -> bool:
        """
        True если запрос слишком короткий или нет бюджета.
        """
        prompt_lower = prompt.lower()

        has_budget = any(
            symbol in prompt for symbol in ["$", "€", "£", "₸", "₽"]
        ) or any(
            word in prompt_lower for word in ["budget", "бюджет", "денег"]
        )

        has_destination = len(prompt.split()) >= 3

        return not (has_budget and has_destination)

    # ── SSE форматирование ──
    # Каждое событие: "data: {json}\n\n"
    # Два \n\n — обязательный разделитель в протоколе SSE

    def _status(self, message: str) -> str:
        data = json.dumps(
            {"type": "status", "message": message},
            ensure_ascii=False
        )
        return f"data: {data}\n\n"

    def _chunk(self, text: str) -> str:
        data = json.dumps(
            {"type": "chunk", "text": text},
            ensure_ascii=False
        )
        return f"data: {data}\n\n"

    def _done(self, plan: dict) -> str:
        data = json.dumps(
            {"type": "done", "plan": plan},
            ensure_ascii=False
        )
        return f"data: {data}\n\n"

    def _error(self, message: str) -> str:
        data = json.dumps(
            {"type": "error", "message": message},
            ensure_ascii=False
        )
        return f"data: {data}\n\n"