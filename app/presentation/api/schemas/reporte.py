from pydantic import BaseModel
from datetime import date


class ReporteCreate(BaseModel):
    periodo: str
    id_tratamiento: int


class ReporteResponse(BaseModel):
    id: int
    fecha_generacion: date
    periodo: str
    porcentaje_cumplimiento: float
    id_tratamiento: int

    class Config:
        from_attributes = True