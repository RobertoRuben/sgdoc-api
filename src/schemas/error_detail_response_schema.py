from pydantic import BaseModel
from typing import Optional

class ErrorDetailResponseSchema(BaseModel):
    field: Optional[str]
    message: str