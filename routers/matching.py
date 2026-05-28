from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from routers.auth import verify_token
from openai import OpenAI
import base64
import os

router = APIRouter(prefix="/matching", tags=["matching"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/analyze")
async def analyze_medication(
    file: UploadFile = File(...),
    payload: dict = Depends(verify_token)
):
    try:
        file_bytes = await file.read()
        image_data = base64.b64encode(file_bytes).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:{file.content_type or 'image/jpeg'};base64,{image_data}"}},
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
        import json
        return json.loads(text.strip())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))