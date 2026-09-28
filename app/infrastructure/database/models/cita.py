from sqlalchemy import Column, Integer, String, Date, ForeignKey

from app.infrastructure.database.database import Base


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    motivo = Column(String(255), nullable=False)
    estado = Column(
        String(20),
        nullable=False,
        default="programada"
    )

    id_paciente = Column(
        Integer,
        ForeignKey("pacientes.id"),
        nullable=False
    )

    id_horario = Column(
        Integer,
        ForeignKey("horarios.id"),
        nullable=False
    )

    id_fisioterapeuta = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )