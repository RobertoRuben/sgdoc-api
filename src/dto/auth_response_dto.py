from pydantic import BaseModel

class AuthResponseDTO(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None
    rol_name: str | None = None
    user_id: int | None = None
    area_id: int | None = None