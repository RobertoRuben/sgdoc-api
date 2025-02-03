from pydantic import BaseModel

class NotAuthenticatedResponse(BaseModel):
    detail: str = "Not authenticated"