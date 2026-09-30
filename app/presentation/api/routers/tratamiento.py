from fastapi import APIRouter, Depends, HTTPException
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
    "/evaluacion/{id_evaluacion}",
    response_model=TratamientoResponse
)
def obtener_tratamiento_por_evaluacion(
    id_evaluacion: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "fisioterapeuta"
        )
    )
):
    tratamiento = TratamientoRepositoryImpl(
        db
    ).get_by_evaluacion(id_evaluacion)

    if not tratamiento:
        raise HTTPException(
            status_code=404,
            detail="La evaluación no tiene un tratamiento"
        )

    return tratamiento

@router.get(
    "/fisioterapeuta/{fisioterapeuta_id}",
    response_model=list[TratamientoResponse]
)
def listar_tratamientos_fisioterapeuta(
    fisioterapeuta_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "fisioterapeuta"
        )
    )
):

    if (
        usuario.rol == "fisioterapeuta"
        and usuario.id != fisioterapeuta_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Solo puede consultar sus propios tratamientos"
        )

    repo = TratamientoRepositoryImpl(db)

    return repo.get_by_fisioterapeuta(
        fisioterapeuta_id
    )

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