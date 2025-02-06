from pydantic import BaseModel

class AuthResponseDTO(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None
    rol_name: str | None = None
    user_id: str | None = None
    area_id: str | None = None