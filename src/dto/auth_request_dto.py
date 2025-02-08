from pydantic import BaseModel, Field

class AuthRequestDTO(BaseModel):
    username: str = Field(min_length=3, description="The username of the user")
    password: str = Field(min_length=8, description="The password of the user")
