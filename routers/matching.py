from fastapi import APIRouter, UploadFile, File, Depends
from services.matching_service import MatchingService
from routers.auth import verify_token

router = APIRouter(prefix="/matching", tags=["matching"])
service = MatchingService()

@router.post("/analyze")
async def analyze_medication(
    file: UploadFile = File(...),
    payload: dict = Depends(verify_token)
):
    file_bytes = await file.read()
    return await service.analyze_medication(file_bytes, file.content_type)
