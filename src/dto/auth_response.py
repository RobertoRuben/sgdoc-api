from pydantic import BaseModel
from typing import Optional

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None