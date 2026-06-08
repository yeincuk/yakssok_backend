from fastapi import APIRouter, Depends
from models.guardian import ConnectRequest, ActionRequest
from services.guardian_service import GuardianService
from routers.auth import verify_token

router = APIRouter(prefix="/guardian", tags=["guardian"])
service = GuardianService()

@router.post("/connect")
async def connect_guardian(req: ConnectRequest, payload: dict = Depends(verify_token)):
    return service.connect_guardian(req, payload["uid"])

@router.get("/records")
async def get_user_records(payload: dict = Depends(verify_token)):
    return service.get_user_records(payload["uid"])

@router.post("/action")
async def guardian_action(req: ActionRequest, payload: dict = Depends(verify_token)):
    return service.guardian_action(req)

@router.get("/status")
async def get_guardian_status(payload: dict = Depends(verify_token)):
    return service.get_guardian_status(payload["uid"])
