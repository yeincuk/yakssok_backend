from pydantic import BaseModel
from typing import List, Optional

class PillCandidate(BaseModel):
    name: str
    confidence: float

class MatchResult(BaseModel):
    match_status: str
    shape: str
    color: str
    imprint: Optional[str] = None
    candidates: List[PillCandidate]
    message: str
