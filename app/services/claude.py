import json 
import anthropic
from app.config import settings

SYSTEM_PROMPT = """You are an expert travel planner. 
When given a destination, duration, budget and interests — 
respond ONLY with a valid JSON object, no other text.

Use this exact schema:
{
  "trip": {
    "title": "string (e.g. Tokyo Adventure)",
    "destination": "string",
    "duration_days": number,
    "total_budget": number,
    "currency": "string (e.g. USD)",
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
      "booking_url": "https://booking.com/search?ss=CITY",
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
- booking_url must be a real Booking.com search URL for that city
- For multi-city trips, include city field in itinerary and hotels
- Respond ONLY with JSON, no markdown, no explanation"""


class ClaudeService:
      
      def __init__(self):
            self.client=anthropic.Anthropic(api_key=settings.anthropic_api_key)
      
      async def generate_trip_plan(self,prompt:str):
            """
        Генерирует план поездки через Claude.
        Это генератор — возвращает события по одному через yield.
        Flutter получает каждое событие сразу.
        """
        
            yield self._status_event("Анализирую направление...")

            full_text=""

            try:
                  with self.client.messages.stream(
                         model="claude-sonnet-4-20250514",
                        max_token=4096,
                        system=SYSTEM_PROMPT,
                        messages=[{"role":"user","content":prompt}]
                  ) as strem:
                        yield self._status_event("Строю маршрут...")
                        for text_chunk in stream.text_stream:
                              full_text+=full_chunk
                              yield self._chunk_event(full_text)
                  yield self._status_event("Финализирую план...")

                  trip_data=json.loads(full_text)
                  yield self._done_event(trip_data)

            except json.JSONDecodeError:
                  yield self._error_event("Не удалось распарсить план. Попробуй снова.")
            except Exception as e:
                  yield self._error_event(str(e))


      def needs_clarification(self, prompt: str) -> bool:
        """
        Проверяет достаточно ли информации в запросе.
        Если нет города или бюджета — просим уточнить.
        """
        prompt_lower = prompt.lower()
        has_budget = any(char in prompt for char in ["$", "€", "£", "₸", "₽"]) or \
                     any(word in prompt_lower for word in ["budget", "бюджет", "денег", "сум"])
        has_destination = len(prompt.split()) > 2

        return not (has_budget and has_destination)


           
      def _status_event(self, message: str) -> str:
        data = json.dumps({"type": "status", "message": message}, ensure_ascii=False)
        return f"data: {data}\n\n"

      def _chunk_event(self, text: str) -> str:
        data = json.dumps({"type": "chunk", "text": text}, ensure_ascii=False)
        return f"data: {data}\n\n"

      def _done_event(self, trip_data: dict) -> str:
        data = json.dumps({"type": "done", "plan": trip_data}, ensure_ascii=False)
        return f"data: {data}\n\n"

      def _error_event(self, message: str) -> str:
        data = json.dumps({"type": "error", "message": message}, ensure_ascii=False)
        return f"data: {data}\n\n"