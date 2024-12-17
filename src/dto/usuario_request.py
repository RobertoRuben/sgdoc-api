from pydantic import BaseModel, Field, field_validator

class UsuarioRequest(BaseModel):
    nombre_usuario: str = Field(..., description="El nombre de usuario es obligatorio")
    contrasena: str = Field(..., description="La contraseña es obligatoria")
    rol_id: int = Field(..., description="El rol es obligatorio")
    trabajador_id: int = Field(..., description="El trabajador es obligatorio")

    @field_validator("nombre_usuario")
    @classmethod
    def nombre_usuario_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre de usuario no debe quedar en blanco")
        return v

    @field_validator("nombre_usuario")
    @classmethod
    def nombre_usuario_not_dot(cls, v):
        if "." in v:
            raise ValueError("El nombre de usuario no debe contener puntos")
        return v


    @field_validator("contrasena")
    @classmethod
    def contrasena_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("La contraseña no debe quedar en blanco")
        return v


    @field_validator("contrasena")
    @classmethod
    def contrasena_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v


    @field_validator("rol_id")
    @classmethod
    def rol_id_not_blank(cls, v):
        if v == "":
            raise ValueError("El rol no debe quedar en blanco")
        return v


    @field_validator("trabajador_id")
    @classmethod
    def trabajador_id_not_blank(cls, v):
        if v == "":
            raise ValueError("El trabajador no debe quedar en blanco")
        return v



