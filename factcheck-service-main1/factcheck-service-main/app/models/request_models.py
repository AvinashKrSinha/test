from pydantic import BaseModel, HttpUrl
from typing import Optional

class ClaimRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[HttpUrl] = None
    file_content: Optional[str] = None  # Base64 encoded content
