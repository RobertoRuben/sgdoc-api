from pydantic import BaseModel
from typing import Optional

class ErrorDetailResponse(BaseModel):
    field: Optional[str]
    message: str