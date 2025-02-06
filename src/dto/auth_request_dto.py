from pydantic import BaseModel

class AuthRequestDTO(BaseModel):
    username: str
    password: str