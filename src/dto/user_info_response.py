from pydantic import BaseModel

class UserInfoResponse(BaseModel):
    id: int
    username: str
    rol_id: int
    is_active: bool
