from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from firebase_config import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "yakssok-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    role: str  # "user" or "guardian"


class LoginRequest(BaseModel):
    email: str
    password: str


def create_token(uid: str, role: str):
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    return jwt.encode({"uid": uid, "role": role, "exp": expire}, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")


@router.post("/register")
async def register(req: RegisterRequest):
    db = get_db()
    # 중복 이메일 확인
    existing = db.collection("users").where("email", "==", req.email).get()
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다")

    hashed_pw = pwd_context.hash(req.password)
    user_ref = db.collection("users").document()
    user_data = {
        "uid": user_ref.id,
        "email": req.email,
        "password": hashed_pw,
        "name": req.name,
        "role": req.role,
        "guardian_id": None,
        "created_at": datetime.utcnow().isoformat()
    }
    user_ref.set(user_data)
    token = create_token(user_ref.id, req.role)
    return {"token": token, "uid": user_ref.id, "name": req.name, "role": req.role}


@router.post("/login")
async def login(req: LoginRequest):
    db = get_db()
    users = db.collection("users").where("email", "==", req.email).get()
    if not users:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸습니다")

    user = users[0].to_dict()
    if not pwd_context.verify(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸습니다")

    token = create_token(user["uid"], user["role"])
    return {"token": token, "uid": user["uid"], "name": user["name"], "role": user["role"]}


@router.get("/me")
async def me(payload: dict = Depends(verify_token)):
    db = get_db()
    user = db.collection("users").document(payload["uid"]).get()
    if not user.exists:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    data = user.to_dict()
    data.pop("password", None)
    return data
