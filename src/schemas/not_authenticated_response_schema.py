from pydantic import BaseModel

class NotAuthenticatedResponseSchema(BaseModel):
    detail: str = "Not authenticated"