from pydantic import BaseModel
from typing import List, Optional

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
