from sqlalchemy import Column, Integer, Date, String, ForeignKey
from app.infrastructure.database.database import Base


class Evolucion(Base):
    __tablename__ = "evoluciones"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    descripcion = Column(String)
    observaciones = Column(String)
    id_sesion = Column(
        Integer,
        ForeignKey("sesiones.id"),
        nullable=False
    )