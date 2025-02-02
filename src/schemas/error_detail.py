from pydantic import BaseModel
from typing import Optional

class ErrorDetail(BaseModel):
    field: Optional[str]
    message: str