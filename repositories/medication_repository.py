from firebase_config import get_db

class MedicationRepository:
    def create_schedule(self, data: dict) -> str:
        db = get_db()
        doc_ref = db.collection("schedules").document()
        data["schedule_id"] = doc_ref.id
        doc_ref.set(data)
        return doc_ref.id

    def get_schedules_by_uid(self, uid: str) -> list:
        db = get_db()
        schedules = db.collection("schedules").where("uid", "==", uid).get()
        return [s.to_dict() for s in schedules]

    def create_record(self, data: dict) -> str:
        db = get_db()
        doc_ref = db.collection("records").document()
        data["record_id"] = doc_ref.id
        doc_ref.set(data)
        return doc_ref.id

    def get_records_by_uid(self, uid: str) -> list:
        db = get_db()
        records = db.collection("records").where("uid", "==", uid).get()
        return [r.to_dict() for r in records]
