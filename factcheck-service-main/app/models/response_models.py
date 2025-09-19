from pydantic import BaseModel
from typing import Any

class VerificationResult(BaseModel):
    status: str
    claim: str
    evidence: Any
    score: float
