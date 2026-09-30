from pydantic import BaseModel, Field
from datetime import date, time


class HorarioSesionResponse(BaseModel):

    id: int

    hora_inicio: time

    hora_fin: time

    class Config:
        from_attributes = True


class SesionCreate(BaseModel):

    fecha: date

    numero_sesion: int = Field(
        ...,
        ge=1
    )

    id_tratamiento: int

    id_horario: int


class SesionReprogramar(BaseModel):

    fecha: date

    id_horario: int

    motivo_reprogramacion: str = Field(
        ...,
        min_length=3,
        max_length=500
    )


class SesionResponse(BaseModel):

    id: int

    fecha: date

    numero_sesion: int

    estado: str

    motivo_reprogramacion: str | None = None

    id_tratamiento: int

    id_horario: int

    horario: HorarioSesionResponse

    class Config:
        from_attributes = True