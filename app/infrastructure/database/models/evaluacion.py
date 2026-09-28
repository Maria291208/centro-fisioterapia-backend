from sqlalchemy import Column, Integer, String, Date, ForeignKey

from app.infrastructure.database.database import Base


class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    diagnostico = Column(String(500), nullable=False)

    id_cita = Column(
        Integer,
        ForeignKey("citas.id"),
        nullable=False
    )