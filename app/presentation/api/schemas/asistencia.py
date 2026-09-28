from pydantic import BaseModel
from datetime import date


class AsistenciaCreate(BaseModel):
    fecha_registro: date
    estado: str
    observaciones: str
    id_sesion: int


class AsistenciaResponse(BaseModel):
    id: int
    fecha_registro: date
    estado: str
    observaciones: str
    id_sesion: int

    class Config:
        from_attributes = True