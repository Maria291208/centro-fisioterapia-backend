from sqlalchemy import Column, Integer, String, Date

from app.infrastructure.database.database import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    ci = Column(String(20), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)