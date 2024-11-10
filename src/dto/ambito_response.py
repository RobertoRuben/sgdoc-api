from pydantic import BaseModel

class AmbitoResponse(BaseModel):
    id : int
    nombre_ambito : str

