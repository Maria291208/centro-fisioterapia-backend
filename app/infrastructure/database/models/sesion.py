from sqlalchemy import Column, Integer, Date, String, ForeignKey
from app.infrastructure.database.database import Base


class Sesion(Base):
    __tablename__ = "sesiones"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    numero_sesion = Column(Integer)
    estado = Column(String, default="prescrita")

    id_tratamiento = Column(
        Integer,
        ForeignKey("tratamientos.id"),
        nullable=False
    )

    id_horario = Column(
        Integer,
        ForeignKey("horarios.id"),
        nullable=False
    )