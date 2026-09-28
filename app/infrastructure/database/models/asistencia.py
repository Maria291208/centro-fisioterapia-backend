from sqlalchemy import Column, Integer, Date, String, ForeignKey
from app.infrastructure.database.database import Base


class Asistencia(Base):
    __tablename__ = "asistencias"

    id = Column(Integer, primary_key=True, index=True)
    fecha_registro = Column(Date)
    estado = Column(String)
    observaciones = Column(String)
    id_sesion = Column(
        Integer,
        ForeignKey("sesiones.id"),
        nullable=False
    )