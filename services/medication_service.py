from datetime import datetime
from models.medication import ScheduleRequest, RecordRequest
from repositories.medication_repository import MedicationRepository

class MedicationService:
    def __init__(self):
        self.repo = MedicationRepository()

    def create_schedule(self, req: ScheduleRequest, uid: str) -> str:
        data = {
            "uid": uid,
            "medications": [m.dict() for m in req.medications],
            "start_date": req.start_date,
            "created_at": datetime.utcnow().isoformat(),
        }
        return self.repo.create_schedule(data)

    def get_schedules(self, uid: str) -> list:
        return self.repo.get_schedules_by_uid(uid)

    def create_record(self, req: RecordRequest, uid: str) -> str:
        data = {
            "uid": uid,
            "schedule_id": req.schedule_id,
            "taken_at": req.taken_at,
            "photo_url": req.photo_url,
            "match_result": req.match_result,
            "guardian_notified": req.guardian_notified,
            "guardian_confirmed": False,
            "guardian_action": None,
            "created_at": datetime.utcnow().isoformat(),
        }
        return self.repo.create_record(data)

    def get_records(self, uid: str) -> list:
        return self.repo.get_records_by_uid(uid)
