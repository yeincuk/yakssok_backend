from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from firebase_config import get_db
from routers.auth import verify_token

router = APIRouter(prefix="/medication", tags=["medication"])


class MedicationItem(BaseModel):
    name: str
    dosage: str
    frequency: str
    times: List[str]
    duration_days: int


class ScheduleRequest(BaseModel):
    medications: List[MedicationItem]
    start_date: str  # YYYY-MM-DD


class RecordRequest(BaseModel):
    schedule_id: str
    taken_at: str
    photo_url: Optional[str] = None
    match_result: str  # "match" | "check" | "fail"
    guardian_notified: bool = False


@router.post("/schedule")
async def create_schedule(req: ScheduleRequest, payload: dict = Depends(verify_token)):
    db = get_db()
    doc_ref = db.collection("schedules").document()
    data = {
        "schedule_id": doc_ref.id,
        "uid": payload["uid"],
        "medications": [m.dict() for m in req.medications],
        "start_date": req.start_date,
        "created_at": datetime.utcnow().isoformat()
    }
    doc_ref.set(data)
    return {"schedule_id": doc_ref.id, "message": "복약 일정이 등록되었습니다"}


@router.get("/schedule")
async def get_schedule(payload: dict = Depends(verify_token)):
    db = get_db()
    schedules = db.collection("schedules").where("uid", "==", payload["uid"]).get()
    return [s.to_dict() for s in schedules]


@router.post("/record")
async def create_record(req: RecordRequest, payload: dict = Depends(verify_token)):
    db = get_db()
    doc_ref = db.collection("records").document()
    data = {
        "record_id": doc_ref.id,
        "uid": payload["uid"],
        "schedule_id": req.schedule_id,
        "taken_at": req.taken_at,
        "photo_url": req.photo_url,
        "match_result": req.match_result,
        "guardian_notified": req.guardian_notified,
        "guardian_confirmed": False,
        "guardian_action": None,
        "created_at": datetime.utcnow().isoformat()
    }
    doc_ref.set(data)
    return {"record_id": doc_ref.id, "message": "복약 기록이 저장되었습니다"}


@router.get("/records")
async def get_records(payload: dict = Depends(verify_token)):
    db = get_db()
    records = db.collection("records").where("uid", "==", payload["uid"]).get()
    return [r.to_dict() for r in records]
