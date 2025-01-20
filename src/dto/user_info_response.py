from pydantic import BaseModel

class UserInfoResponse(BaseModel):
    id: int
    username: str
    rol_id: int
    rol_name: str
    area_id: int
    is_active: bool

