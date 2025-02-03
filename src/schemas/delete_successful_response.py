from pydantic import BaseModel

class DeleteSuccessfulResponse(BaseModel):
    message: str