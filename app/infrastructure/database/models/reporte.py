from sqlalchemy import Column, Integer, Date, String, Float, ForeignKey
from app.infrastructure.database.database import Base


class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, index=True)
    fecha_generacion = Column(Date)
    periodo = Column(String)
    porcentaje_cumplimiento = Column(Float)
    id_tratamiento = Column(
        Integer,
        ForeignKey("tratamientos.id"),
        nullable=False
    )