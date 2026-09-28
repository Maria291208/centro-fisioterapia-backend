from fastapi import FastAPI

from app.infrastructure.database.database import Base, engine

from app.infrastructure.database.models.usuario import Usuario
from app.infrastructure.database.models.paciente import Paciente

from app.presentation.api.routers import sesion, tratamiento, usuario, paciente, horario, cita, evaluacion
from app.presentation.api.routers import (
    evolucion,
    asistencia,
    reporte
)
from app.infrastructure.database.models.horario import Horario

from app.infrastructure.database.models.horario import Horario
from app.infrastructure.database.models.cita import Cita

from app.infrastructure.database.models.evaluacion import Evaluacion

from app.infrastructure.database.models.tratamiento import Tratamiento
from app.infrastructure.database.models.sesion import Sesion
from app.infrastructure.database.models.tratamiento import Tratamiento
from app.infrastructure.database.models.sesion import Sesion

from app.infrastructure.database.models.evolucion import Evolucion
from app.infrastructure.database.models.asistencia import Asistencia
from app.infrastructure.database.models.reporte import Reporte
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sistema de Gestión - Centro de Fisioterapia"
)


app.include_router(usuario.router)
app.include_router(paciente.router)
app.include_router(horario.router)
app.include_router(cita.router)
app.include_router(evaluacion.router)
app.include_router(sesion.router)
app.include_router(tratamiento.router)
app.include_router(evolucion.router)
app.include_router(asistencia.router)
app.include_router(reporte.router)