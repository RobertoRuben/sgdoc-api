from pydantic import BaseModel

class NotAuthenticated(BaseModel):
    detail: str = "Not authenticated"