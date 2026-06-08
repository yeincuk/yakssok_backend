from datetime import datetime
from fastapi import HTTPException
from models.guardian import ConnectRequest, ActionRequest
from repositories.guardian_repository import GuardianRepository

class GuardianService:
    def __init__(self):
        self.repo = GuardianRepository()

    def connect_guardian(self, req: ConnectRequest, guardian_uid: str):
        users = self.repo.find_user_by_email(req.user_email)
        if not users:
            raise HTTPException(status_code=404, detail="해당 이메일의 사용자를 찾을 수 없습니다")
        user = users[0]
        if user["role"] != "user":
            raise HTTPException(status_code=400, detail="보호 대상 사용자가 아닙니다")
        self.repo.link_guardian(user["uid"], guardian_uid)
        return {"message": f"{user['name']}님과 연결되었습니다", "user_id": user["uid"]}

    def get_user_records(self, guardian_uid: str):
        guardian = self.repo.get_guardian(guardian_uid)
        linked_user_id = guardian.get("linked_user_id")
        if not linked_user_id:
            raise HTTPException(status_code=404, detail="연결된 사용자가 없습니다")
        records = self.repo.get_records_by_uid(linked_user_id)
        records.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return records

    def guardian_action(self, req: ActionRequest):
        record_ref = self.repo.get_record_by_id(req.record_id)
        record = record_ref.get()
        if not record.exists:
            raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")
        record_ref.update({
            "guardian_confirmed": True,
            "guardian_action": req.action,
            "guardian_action_at": datetime.utcnow().isoformat()
        })
        action_messages = {
            "confirmed": "복용 가능합니다",
            "retake": "다시 촬영해 주세요",
            "pharmacist": "약사 확인이 필요합니다. 복용을 보류해 주세요",
            "call": "보호자가 전화를 요청했습니다"
        }
        return {
            "message": action_messages.get(req.action, "조치가 완료되었습니다"),
            "action": req.action,
            "record_id": req.record_id
        }

    def get_guardian_status(self, guardian_uid: str):
        guardian = self.repo.get_guardian(guardian_uid)
        linked_user_id = guardian.get("linked_user_id")
        if not linked_user_id:
            return {"connected": False}
        user = self.repo.get_user_by_uid(linked_user_id)
        records = self.repo.get_records_by_uid(linked_user_id)
        pending = [r for r in records if not r.get("guardian_confirmed")]
        confirmed = [r for r in records if r.get("guardian_action") == "confirmed"]
        needs_check = [r for r in records if r.get("match_result") in ["check", "fail"]]
        return {
            "connected": True,
            "user_name": user.get("name"),
            "pending_count": len(pending),
            "confirmed_count": len(confirmed),
            "needs_check_count": len(needs_check)
        }
