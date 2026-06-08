from pydantic import BaseModel

class ConnectRequest(BaseModel):
    user_email: str

class ActionRequest(BaseModel):
    record_id: str
    action: str  # "confirmed" | "retake" | "pharmacist" | "call"
