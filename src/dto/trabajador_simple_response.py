from pydantic import BaseModel

class TrabajadorSimpleReponse(BaseModel):
    id: int
    nombres: str