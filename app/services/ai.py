import json
from typing import Any
from PIL import Image
from google import genai
from google.genai import types
from app.config import settings
from app.services.catalog import candidates

class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key) if settings.gemini_api_key else None

    def _prompt(self, planner: str, data: dict[str, Any], catalog: list[tuple]):
        catalog_text = "\n".join(f"{i+1}. {x[0]} | {x[1]} | ₹{x[2]} | {x[3]} | {x[4]}" for i, x in enumerate(catalog))
        return f'''You are PocketSmart AI, a careful budget recommendation assistant.
Planner: {planner}
User input: {json.dumps(data, ensure_ascii=False)}
Candidate catalog (links are search/product destinations, not live inventory):
{catalog_text}

Return ONLY valid JSON with this shape:
{{"summary":"...","allocated_total":number,"items":[{{"category":"...","name":"...","estimated_price":number,"platform":"...","url":"...","reason":"..."}}],"tips":["..."]}}
Rules: stay within the stated budget; never invent live stock, exact availability, ratings, or current prices; use only catalog URLs; if an item has price 0, explain that it is a search/service category and estimate a sensible allocation instead. Keep 3-8 useful items.'''

    def fallback(self, planner: str, data: dict[str, Any], image: Image.Image | None = None):
        budget = float(data["budget"])
        rows = candidates(planner, budget)
        if planner == "home":
            weights = [0.18, 0.18, 0.28, 0.16, 0.12, 0.08]
            allocations = [budget*w for w in weights[:len(rows)]]
            items = [{"category": r[0], "name": r[1], "estimated_price": min(float(r[2]), round(a)), "platform": r[3], "url": r[4], "reason": f"Fits a {data.get('style','modern')} style and the available budget."} for r,a in zip(rows, allocations)]
        elif planner == "party":
            per_guest = budget / max(int(data["guests"]), 1)
            items = [{"category": r[0], "name": r[1], "estimated_price": round(budget*0.35 if r[0]=="Food" else budget*0.15, 2), "platform": r[3], "url": r[4], "reason": f"Starting point for {data['guests']} guests at about ₹{per_guest:.0f} per guest."} for r in rows]
        else:
            items = [{"category": r[0], "name": r[1], "estimated_price": float(r[2]), "platform": r[3], "url": r[4], "reason": f"Selected for the {data.get('occasion','special occasion')} and {data.get('style','classic')} style."} for r in rows if r[2] <= budget][:4]
        total = min(sum(x["estimated_price"] for x in items), budget)
        return {"summary": "Starter recommendations generated from the built-in catalog. Add a Gemini API key for personalized AI reasoning.", "allocated_total": round(total,2), "items": items, "tips": ["Verify the final price and availability on the destination platform before purchasing.", "Keep a small contingency amount for delivery, taxes, or last-minute changes."]}

    def generate(self, planner: str, data: dict[str, Any], image_bytes: bytes | None = None, mime_type: str | None = None):
        if not self.client:
            return self.fallback(planner, data), "fallback"
        try:
            contents: list[Any] = [self._prompt(planner, data, candidates(planner, float(data["budget"]))) ]
            if image_bytes:
                contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type or "image/jpeg"))
                contents[0] += "\nAn outfit image is attached. For jewelry, use visible colors/style only; do not identify the person."
            response = self.client.models.generate_content(model=settings.gemini_model, contents=contents, config=types.GenerateContentConfig(temperature=0.4, response_mime_type="application/json"))
            parsed = json.loads(response.text)
            return parsed, "gemini"
        except Exception:
            return self.fallback(planner, data, None), "fallback"

ai_service = AIService()
