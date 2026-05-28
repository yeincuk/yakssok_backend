from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from firebase_config import get_db
from routers.auth import verify_token

router = APIRouter(prefix="/guardian", tags=["guardian"])


class ConnectRequest(BaseModel):
    user_email: str  # 보호자가 연결할 사용자 이메일


class ActionRequest(BaseModel):
    record_id: str
    action: str  # "confirmed" | "retake" | "pharmacist" | "call"


@router.post("/connect")
async def connect_guardian(req: ConnectRequest, payload: dict = Depends(verify_token)):
    db = get_db()
    # 사용자 찾기
    users = db.collection("users").where("email", "==", req.user_email).get()
    if not users:
        raise HTTPException(status_code=404, detail="해당 이메일의 사용자를 찾을 수 없습니다")

    user = users[0].to_dict()
    if user["role"] != "user":
        raise HTTPException(status_code=400, detail="보호 대상 사용자가 아닙니다")

    # 보호자 연결
    db.collection("users").document(user["uid"]).update({
        "guardian_id": payload["uid"]
    })
    db.collection("users").document(payload["uid"]).update({
        "linked_user_id": user["uid"]
    })

    return {"message": f"{user['name']}님과 연결되었습니다", "user_id": user["uid"]}


@router.get("/records")
async def get_user_records(payload: dict = Depends(verify_token)):
    db = get_db()
    # 보호자가 연결된 사용자 찾기
    guardian = db.collection("users").document(payload["uid"]).get().to_dict()
    linked_user_id = guardian.get("linked_user_id")
    if not linked_user_id:
        raise HTTPException(status_code=404, detail="연결된 사용자가 없습니다")

    records = db.collection("records").where("uid", "==", linked_user_id).get()
    result = [r.to_dict() for r in records]
    result.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return result


@router.post("/action")
async def guardian_action(req: ActionRequest, payload: dict = Depends(verify_token)):
    db = get_db()
    record_ref = db.collection("records").document(req.record_id)
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


@router.get("/status")
async def get_guardian_status(payload: dict = Depends(verify_token)):
    db = get_db()
    guardian = db.collection("users").document(payload["uid"]).get().to_dict()
    linked_user_id = guardian.get("linked_user_id")
    if not linked_user_id:
        return {"connected": False}

    user = db.collection("users").document(linked_user_id).get().to_dict()
    records = db.collection("records").where("uid", "==", linked_user_id).get()
    record_list = [r.to_dict() for r in records]

    pending = [r for r in record_list if not r.get("guardian_confirmed")]
    confirmed = [r for r in record_list if r.get("guardian_action") == "confirmed"]
    needs_check = [r for r in record_list if r.get("match_result") in ["check", "fail"]]

    return {
        "connected": True,
        "user_name": user.get("name"),
        "pending_count": len(pending),
        "confirmed_count": len(confirmed),
        "needs_check_count": len(needs_check)
    }
