from pydantic import BaseModel
from datetime import date


class PacienteCreate(BaseModel):
    nombre: str
    apellido: str
    ci: str
    telefono: str
    direccion: str
    fecha_nacimiento: date
    username: str
    password: str


class PacienteUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    ci: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    fecha_nacimiento: date | None = None


class PacienteResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    ci: str
    telefono: str
    direccion: str
    fecha_nacimiento: date

    class Config:
        from_attributes = True