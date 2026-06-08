from pydantic import BaseModel

class IdentifyRequest(BaseModel):
    question: str = "이 약이 무엇인지 설명해줘"
