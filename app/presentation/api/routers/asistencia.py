from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.infrastructure.database.repositories.asistencia_repository import (
    AsistenciaRepositoryImpl
)

from app.infrastructure.database.repositories.sesion_repository import (
    SesionRepositoryImpl
)

from app.infrastructure.database.repositories.tratamiento_repository import (
    TratamientoRepositoryImpl
)

from app.application.use_cases.asistencia.registrar_asistencia import (
    RegistrarAsistencia
)

from app.presentation.api.schemas.asistencia import (
    AsistenciaCreate,
    AsistenciaResponse
)

from app.presentation.api.dependencies import requerir_roles


router = APIRouter(
    prefix="/asistencias",
    tags=["Asistencias"]
)


@router.post(
    "/",
    response_model=AsistenciaResponse
)
def registrar_asistencia(
    datos: AsistenciaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "fisioterapeuta"
        )
    )
):

    asistencia_repo = AsistenciaRepositoryImpl(db)
    sesion_repo = SesionRepositoryImpl(db)
    tratamiento_repo = TratamientoRepositoryImpl(db)

    caso = RegistrarAsistencia(
        asistencia_repo,
        sesion_repo,
        tratamiento_repo
    )

    return caso.ejecutar(datos)


@router.get(
    "/",
    response_model=list[AsistenciaResponse]
)
def listar_asistencias(
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "fisioterapeuta"
        )
    )
):

    repo = AsistenciaRepositoryImpl(db)

    return repo.get_all()