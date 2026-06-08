from fastapi import APIRouter, UploadFile, File, Depends
from services.ocr_service import OcrService
from routers.auth import verify_token

router = APIRouter(prefix="/ocr", tags=["ocr"])
service = OcrService()

@router.post("/scan")
async def scan_prescription(
    file: UploadFile = File(...),
    payload: dict = Depends(verify_token)
):
    file_bytes = await file.read()
    return await service.scan_prescription(file_bytes, file.content_type)
