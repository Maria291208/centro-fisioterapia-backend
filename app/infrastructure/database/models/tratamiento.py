from sqlalchemy import Column, Integer, Date, String, ForeignKey
from app.infrastructure.database.database import Base


class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id = Column(Integer, primary_key=True, index=True)

    fecha_inicio = Column(Date)

    fecha_fin = Column(Date)

    objetivo = Column(String)

    numero_sesiones = Column(
        Integer,
        nullable=False
    )

    estado = Column(
        String,
        default="activo"
    )

    id_evaluacion = Column(
        Integer,
        ForeignKey("evaluaciones.id"),
        nullable=False
    )