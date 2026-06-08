from fastapi import APIRouter, File, UploadFile, Form
from services.identify_service import IdentifyService

router = APIRouter()
service = IdentifyService()

@router.post("/identify")
async def identify_pill(
    image: UploadFile = File(...),
    question: str = Form(default="이 약이 무엇인지 설명해줘")
):
    image_bytes = await image.read()
    return await service.identify_pill(image_bytes, image.filename, image.content_type, question)
