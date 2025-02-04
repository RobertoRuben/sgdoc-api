from pydantic import BaseModel

class PatchSuccesfulResponseSchema(BaseModel):
    message: str