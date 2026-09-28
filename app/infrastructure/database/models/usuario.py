from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.infrastructure.database.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rol = Column(String, default="paciente")
    active = Column(Boolean, default=True)

    id_paciente = Column(
        Integer,
        ForeignKey("pacientes.id"),
        nullable=True
    )