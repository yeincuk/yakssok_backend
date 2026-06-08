import base64
import json
import os
from fastapi import HTTPException
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OcrService:
    async def scan_prescription(self, file_bytes: bytes, content_type: str):
        try:
            image_data = base64.b64encode(file_bytes).decode("utf-8")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:{content_type or 'image/jpeg'};base64,{image_data}"}},
                        {"type": "text", "text": 'Return JSON only, no other text. Extract medicine info from this prescription image. Format: {"medications":[{"name":"medicine name","dosage":"amount","frequency":"times per day","times":["time"],"duration_days":days}],"total_medications":count,"duration_days":days,"ocr_status":"success"} If no prescription: {"medications":[],"ocr_status":"no_prescription_found"}'}
                    ]
                }],
                max_tokens=1000
            )
            text = response.choices[0].message.content.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text.strip())
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
