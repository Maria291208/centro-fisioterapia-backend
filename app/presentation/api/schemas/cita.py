from datetime import date, time

from pydantic import BaseModel


class HorarioResponse(BaseModel):
    id: int
    hora_inicio: time
    hora_fin: time

    class Config:
        from_attributes = True


class CitaCreate(BaseModel):
    fecha: date
    motivo: str
    id_paciente: int
    id_horario: int
    id_fisioterapeuta: int


class CitaUpdate(BaseModel):
    fecha: date | None = None
    motivo: str | None = None
    id_horario: int | None = None
    id_fisioterapeuta: int | None = None
    estado: str | None = None


class CitaResponse(BaseModel):
    id: int
    fecha: date
    motivo: str
    estado: str
    id_paciente: int
    id_horario: int
    id_fisioterapeuta: int
    horario: HorarioResponse

    class Config:
        from_attributes = True