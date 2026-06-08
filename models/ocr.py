from pydantic import BaseModel
from typing import List

class OcrMedicationItem(BaseModel):
    name: str
    dosage: str
    frequency: str
    times: List[str]
    duration_days: int

class OcrResult(BaseModel):
    medications: List[OcrMedicationItem]
    total_medications: int
    duration_days: int
    ocr_status: str
