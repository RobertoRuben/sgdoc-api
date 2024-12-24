from pydantic import BaseModel, field_validator, Field

class DocumentoRequest(BaseModel):
    documento_bytes: bytes = Field(..., description="El documento debe ser un archivo")
    nombre: str = Field(..., description="El nombre del documento no puede estar vacío")
    folios: int = Field(..., description="El número de folios debe ser mayor a cero")
    asunto: str = Field(..., description="El asunto del documento no puede estar vacío")
    ambito_id: int = Field(..., description="El id del ámbito debe ser mayor a cero", ge=1)
    categoria_id: int = Field(..., description="El id de la categoría debe ser mayor a cero", ge=1)
    caserio_id: int | None = Field(None, description="El id del caserío debe ser mayor a cero", ge=1)
    centro_poblado_id: int | None = Field(None, description="El id del centro poblado debe ser mayor a cero", ge=1)

    @field_validator("documento_bytes")
    def documento_bytes_not_empty(cls, v):
        if not v:
            raise ValueError("El documento no puede estar vacío")
        return v

    @field_validator("nombre")
    def nombre_not_empty(cls, v):
        if not v:
            raise ValueError("El nombre del documento no puede estar vacío")
        return v

    @field_validator("folios")
    def folios_getter_than_zero(cls, v):
        if v < 1:
            raise ValueError("El número de folios debe ser mayor a cero")
        return v

    @field_validator("folios")
    def folios_not_string(cls, v):
        if isinstance(v, str):
            raise ValueError("El número de folios no puede ser una cadena de texto")
        return v

    @field_validator("asunto")
    def asunto_not_empty(cls, v):
        if not v:
            raise ValueError("El asunto del documento no puede estar vacío")
        return v

    @field_validator("ambito_id")
    def ambito_id_getter_than_zero(cls, v):
        if v < 1:
            raise ValueError("El id del ámbito debe ser mayor a cero")
        return v

    @field_validator("ambito_id")
    def ambito_id_not_string(cls, v):
        if isinstance(v, str):
            raise ValueError("El id del ámbito no puede ser una cadena de texto")
        return v

    @field_validator("categoria_id")
    def categoria_id_getter_than_zero(cls, v):
        if v < 1:
            raise ValueError("El id de la categoría debe ser mayor a cero")
        return v

    @field_validator("categoria_id")
    def categoria_id_not_string(cls, v):
        if isinstance(v, str):
            raise ValueError("El id de la categoría no puede ser una cadena de texto")
        return v

    @field_validator("caserio_id")
    def caserio_id_getter_than_zero(cls, v):
        if v is not None and v < 1:
            raise ValueError("El id del caserío debe ser mayor a cero")
        return v

    @field_validator("caserio_id")
    def caserio_id_not_string(cls, v):
        if isinstance(v, str):
            raise ValueError("El id del caserío no puede ser una cadena de texto")
        return v

    @field_validator("centro_poblado_id")
    def centro_poblado_id_getter_and_equal_than_zero(cls, v):
        if v is not None and v < 1:
            raise ValueError("El id del centro poblado debe ser mayor a cero")
        return v

    @field_validator("centro_poblado_id")
    def centro_poblado_id_not_string(cls, v):
        if isinstance(v, str):
            raise ValueError("El id del centro poblado no puede ser una cadena de texto")
        return v
