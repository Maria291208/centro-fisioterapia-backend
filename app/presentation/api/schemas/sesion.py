from pydantic import BaseModel
from datetime import date


class SesionCreate(BaseModel):
    fecha: date
    numero_sesion: int
    id_tratamiento: int
    id_horario: int


class SesionResponse(BaseModel):
    id: int
    fecha: date
    numero_sesion: int
    estado: str
    id_tratamiento: int
    id_horario: int

    class Config:
        from_attributes = True