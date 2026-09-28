from sqlalchemy import Column, Integer, Time, String

from app.infrastructure.database.database import Base


class Horario(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado = Column(
        String(20),
        nullable=False,
        default="disponible"
    )