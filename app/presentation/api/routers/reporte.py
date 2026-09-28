from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.infrastructure.database.repositories.reporte_repository import ReporteRepositoryImpl
from app.infrastructure.database.repositories.tratamiento_repository import TratamientoRepositoryImpl
from app.infrastructure.database.repositories.sesion_repository import SesionRepositoryImpl
from app.infrastructure.database.repositories.asistencia_repository import AsistenciaRepositoryImpl

from app.application.use_cases.reporte.generar_reporte import GenerarReporte

from app.presentation.api.schemas.reporte import (
    ReporteCreate,
    ReporteResponse
)

from app.presentation.api.dependencies import requerir_roles


router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)


@router.post(
    "/",
    response_model=ReporteResponse
)
def generar_reporte(
    datos: ReporteCreate,
    db: Session = Depends(get_db),
    usuario=Depends(requerir_roles("administrador", "fisioterapeuta"))
):

    reporte_repo = ReporteRepositoryImpl(db)
    tratamiento_repo = TratamientoRepositoryImpl(db)
    sesion_repo = SesionRepositoryImpl(db)
    asistencia_repo = AsistenciaRepositoryImpl(db)

    caso = GenerarReporte(
        reporte_repo,
        tratamiento_repo,
        sesion_repo,
        asistencia_repo
    )

    return caso.ejecutar(datos)


@router.get(
    "/",
    response_model=list[ReporteResponse]
)
def listar_reportes(
    db: Session = Depends(get_db),
    usuario=Depends(requerir_roles("administrador", "fisioterapeuta"))
):

    repo = ReporteRepositoryImpl(db)

    return repo.get_all()