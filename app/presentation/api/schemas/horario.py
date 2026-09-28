from datetime import time

from pydantic import BaseModel


class HorarioCreate(BaseModel):
    hora_inicio: time
    hora_fin: time
    estado: str = "disponible"


class HorarioUpdate(BaseModel):
    hora_inicio: time | None = None
    hora_fin: time | None = None
    estado: str | None = None


class HorarioResponse(BaseModel):
    id: int
    hora_inicio: time
    hora_fin: time
    estado: str

    class Config:
        from_attributes = True