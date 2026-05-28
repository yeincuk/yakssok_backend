from fastapi import APIRouter, File, UploadFile, Form
import httpx
import os

router = APIRouter()

COLAB_URL = os.getenv("COLAB_IDENTIFY_URL", "http://211.105.65.14:8080")

@router.post("/identify")
async def identify_pill(
    image: UploadFile = File(...),
    question: str = Form(default="이 약이 무엇인지 설명해줘")
):
    image_bytes = await image.read()
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{COLAB_URL}/identify",
            files={"image": (image.filename, image_bytes, image.content_type)},
            data={"question": question},
        )
        return response.json()
