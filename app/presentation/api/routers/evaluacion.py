from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.infrastructure.database.repositories.evaluacion_repository import (
    EvaluacionRepository
)

from app.infrastructure.database.repositories.cita_repository import (
    CitaRepository
)

from app.application.use_cases.evaluacion.registrar_evaluacion import (
    RegistrarEvaluacion
)

from app.presentation.api.schemas.evaluacion import (
    EvaluacionCreate,
    EvaluacionResponse
)

from app.presentation.api.dependencies import requerir_roles


router = APIRouter(
    prefix="/evaluaciones",
    tags=["Evaluaciones"]
)


@router.post(
    "/",
    response_model=EvaluacionResponse,
    status_code=201
)
def registrar_evaluacion(
    datos: EvaluacionCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "fisioterapeuta"
        )
    )
):
 return RegistrarEvaluacion(
    EvaluacionRepository(db),
    CitaRepository(db)
).ejecutar(datos, usuario)