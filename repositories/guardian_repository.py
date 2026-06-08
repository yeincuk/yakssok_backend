from firebase_config import get_db

class GuardianRepository:
    def find_user_by_email(self, email: str):
        db = get_db()
        users = db.collection("users").where("email", "==", email).get()
        return [u.to_dict() for u in users]

    def link_guardian(self, user_uid: str, guardian_uid: str):
        db = get_db()
        db.collection("users").document(user_uid).update({
            "guardian_id": guardian_uid
        })
        db.collection("users").document(guardian_uid).update({
            "linked_user_id": user_uid
        })

    def get_guardian(self, guardian_uid: str):
        db = get_db()
        return db.collection("users").document(guardian_uid).get().to_dict()

    def get_records_by_uid(self, uid: str):
        db = get_db()
        records = db.collection("records").where("uid", "==", uid).get()
        return [r.to_dict() for r in records]

    def get_record_by_id(self, record_id: str):
        db = get_db()
        return db.collection("records").document(record_id)

    def get_user_by_uid(self, uid: str):
        db = get_db()
        return db.collection("users").document(uid).get().to_dict()
