from pydantic import BaseModel
from datetime import date


class TratamientoCreate(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    objetivo: str
    id_evaluacion: int


class TratamientoUpdate(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    objetivo: str
    estado: str


class TratamientoResponse(BaseModel):
    id: int
    fecha_inicio: date
    fecha_fin: date
    objetivo: str
    estado: str
    id_evaluacion: int

    class Config:
        from_attributes = True