from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, ocr, medication, matching, guardian, identify

app = FastAPI(title="약쏙 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "https://sturdy-visible-vacancy.ngrok-free.dev",
    ],
    allow_origin_regex="https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(ocr.router)
app.include_router(medication.router)
app.include_router(matching.router)
app.include_router(guardian.router)
app.include_router(identify.router)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}
