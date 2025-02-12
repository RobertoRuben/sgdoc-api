from pydantic import BaseModel, Field, field_validator, model_validator

class DashboardFilterRequestDTO(BaseModel):
    start_year: int | None = Field(None, description="Año de inicio. Si es nulo se utiliza el año actual.")
    end_year: int | None = Field(None, description="Año de fin. Si es nulo se utiliza el año actual.")
    start_year_month: int | None = Field(None, description="Mes de inicio. Si es nulo se toma el valor 1")
    end_year_month: int | None = Field(None, description="Mes de fin. Si es nulo se toma el valor 12")


    @field_validator("start_year")
    def validate_start_year(cls, v):
        if v is not None and v <=2024:
            raise ValueError("El año de inicio debe ser mayor a 2024")
        return v


    @model_validator(mode="after")
    def validate_years(cls, model: "DashboardFilterRequestDTO"):
        if model.start_year is not None and model.end_year is not None:
            if model.end_year < model.start_year:
                raise ValueError("El año de fin no debe ser menor que el año de inicio")
        return model


    @field_validator("start_year_month")
    def validate_start_year_month(cls, v):
        if v is not None and (v < 1 or v > 12):
            raise ValueError("El mes de inicio debe estar entre 1 y 12")
        return v


    @model_validator(mode="after")
    def validate_months(cls, model: "DashboardFilterRequestDTO"):
        if model.start_year_month is not None and model.end_year_month is not None:
            if model.end_year_month < model.start_year_month:
                raise ValueError("El mes de fin no debe ser menor que el mes de inicio")
        return model
