from pydantic import BaseModel


class FactCheckResponse(BaseModel):
    verdict: str
    confidence: float
    rationale: str

from pydantic import BaseModel, HttpUrl


class FactCheckRequest(BaseModel):
    query: str
    source_url: HttpUrl | None = None


