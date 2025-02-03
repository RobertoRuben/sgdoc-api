from pydantic import BaseModel

class DeleteSuccessfulResponseSchema(BaseModel):
    message: str