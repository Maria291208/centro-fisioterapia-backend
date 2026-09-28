from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.infrastructure.database.repositories.evolucion_repository import EvolucionRepositoryImpl
from app.infrastructure.database.repositories.sesion_repository import SesionRepositoryImpl

from app.application.use_cases.evolucion.registrar_evolucion import RegistrarEvolucion

from app.presentation.api.schemas.evolucion import (
    EvolucionCreate,
    EvolucionResponse
)

from app.presentation.api.dependencies import requerir_roles


router = APIRouter(
    prefix="/evoluciones",
    tags=["Evoluciones"]
)


@router.post(
    "/",
    response_model=EvolucionResponse
)
def registrar_evolucion(
    datos: EvolucionCreate,
    db: Session = Depends(get_db),
    usuario=Depends(requerir_roles("administrador", "fisioterapeuta"))
):

    evolucion_repo = EvolucionRepositoryImpl(db)
    sesion_repo = SesionRepositoryImpl(db)

    caso = RegistrarEvolucion(
        evolucion_repo,
        sesion_repo
    )

    return caso.ejecutar(datos)


@router.get(
    "/",
    response_model=list[EvolucionResponse]
)
def listar_evoluciones(
    db: Session = Depends(get_db),
    usuario=Depends(requerir_roles("administrador", "fisioterapeuta"))
):

    repo = EvolucionRepositoryImpl(db)

    return repo.get_all()