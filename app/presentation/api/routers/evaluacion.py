from http.client import HTTPException

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

@router.get(
    "/cita/{id_cita}",
    response_model=EvaluacionResponse
)
def obtener_evaluacion_por_cita(
    id_cita: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "fisioterapeuta"
        )
    )
):
    evaluacion = EvaluacionRepository(
        db
    ).get_by_cita(id_cita)

    if not evaluacion:
        raise HTTPException(
            status_code=404,
            detail="La cita no tiene una evaluación inicial"
        )

    return evaluacion