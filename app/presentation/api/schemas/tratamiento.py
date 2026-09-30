from pydantic import BaseModel, Field
from datetime import date


class TratamientoCreate(BaseModel):

    fecha_inicio: date

    fecha_fin: date

    objetivo: str

    numero_sesiones: int = Field(
        ...,
        ge=1
    )

    id_evaluacion: int


class TratamientoUpdate(BaseModel):

    fecha_inicio: date

    fecha_fin: date

    objetivo: str

    numero_sesiones: int = Field(
        ...,
        ge=1
    )

    estado: str


class TratamientoResponse(BaseModel):

    id: int

    fecha_inicio: date

    fecha_fin: date

    objetivo: str

    numero_sesiones: int

    estado: str

    id_evaluacion: int

    class Config:
        from_attributes = True