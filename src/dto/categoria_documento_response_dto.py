from pydantic import BaseModel

class CategoriaDocumentoResponseDTO(BaseModel):
    id: int
    nombre_categoria: str