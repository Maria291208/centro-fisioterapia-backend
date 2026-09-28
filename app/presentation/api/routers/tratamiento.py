from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.tratamiento_repository import TratamientoRepositoryImpl
from app.infrastructure.database.repositories.evaluacion_repository import EvaluacionRepositoryImpl

from app.application.use_cases.tratamiento.registrar_tratamiento import RegistrarTratamiento

from app.presentation.api.schemas.tratamiento import (
    TratamientoCreate,
    TratamientoResponse
)

from app.presentation.api.dependencies import requerir_roles


router = APIRouter(
    prefix="/tratamientos",
    tags=["Tratamientos"]
)


@router.post(
    "/",
    response_model=TratamientoResponse
)
def registrar_tratamiento(
    datos: TratamientoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(requerir_roles("administrador", "fisioterapeuta"))
):

    tratamiento_repo = TratamientoRepositoryImpl(db)
    evaluacion_repo = EvaluacionRepositoryImpl(db)

    caso = RegistrarTratamiento(
        tratamiento_repo,
        evaluacion_repo
    )

    return caso.ejecutar(datos)


@router.get(
    "/",
    response_model=list[TratamientoResponse]
)
def listar_tratamientos(
    db: Session = Depends(get_db),
    usuario=Depends(requerir_roles("administrador", "fisioterapeuta"))
):

    repo = TratamientoRepositoryImpl(db)

    return repo.get_all()


@router.get(
    "/{id}",
    response_model=TratamientoResponse
)
def obtener_tratamiento(
    id: int,
    db: Session = Depends(get_db),
    usuario=Depends(requerir_roles("administrador", "fisioterapeuta"))
):

    repo = TratamientoRepositoryImpl(db)

    return repo.get_by_id(id)