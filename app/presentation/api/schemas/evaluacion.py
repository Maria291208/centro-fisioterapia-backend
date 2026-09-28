from datetime import date

from pydantic import BaseModel


class EvaluacionCreate(BaseModel):
    fecha: date
    diagnostico: str
    id_cita: int


class EvaluacionUpdate(BaseModel):
    fecha: date | None = None
    diagnostico: str | None = None


class EvaluacionResponse(BaseModel):
    id: int
    fecha: date
    diagnostico: str
    id_cita: int

    class Config:
        from_attributes = True