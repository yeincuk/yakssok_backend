import base64
import json
import os
from fastapi import HTTPException
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MatchingService:
    async def analyze_medication(self, file_bytes: bytes, content_type: str):
        try:
            image_data = base64.b64encode(file_bytes).decode("utf-8")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:{content_type or 'image/jpeg'};base64,{image_data}"}},
                        {"type": "text", "text": 'Analyze this pill image and return JSON only. {"match_status": "high" or "low" or "unknown", "shape": "pill shape", "color": "pill color", "imprint": "text on pill if any", "candidates": [{"name": "medicine name", "confidence": 0.0}], "message": "brief explanation"}'}
                    ]
                }],
                max_tokens=500
            )
            text = response.choices[0].message.content.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text.strip())
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
