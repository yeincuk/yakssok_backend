from fastapi import APIRouter, Depends
from models.medication import ScheduleRequest, RecordRequest
from services.medication_service import MedicationService
from routers.auth import verify_token

router = APIRouter(prefix="/medication", tags=["medication"])
service = MedicationService()

@router.post("/schedule")
async def create_schedule(req: ScheduleRequest, payload: dict = Depends(verify_token)):
    schedule_id = service.create_schedule(req, payload["uid"])
    return {"schedule_id": schedule_id, "message": "복약 일정이 등록되었습니다"}

@router.get("/schedule")
async def get_schedule(payload: dict = Depends(verify_token)):
    return service.get_schedules(payload["uid"])

@router.post("/record")
async def create_record(req: RecordRequest, payload: dict = Depends(verify_token)):
    record_id = service.create_record(req, payload["uid"])
    return {"record_id": record_id, "message": "복약 기록이 저장되었습니다"}

@router.get("/records")
async def get_records(payload: dict = Depends(verify_token)):
    return service.get_records(payload["uid"])
