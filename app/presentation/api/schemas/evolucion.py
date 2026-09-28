from pydantic import BaseModel
from datetime import date


class EvolucionCreate(BaseModel):
    fecha: date
    descripcion: str
    observaciones: str
    id_sesion: int


class EvolucionResponse(BaseModel):
    id: int
    fecha: date
    descripcion: str
    observaciones: str
    id_sesion: int

    class Config:
        from_attributes = True