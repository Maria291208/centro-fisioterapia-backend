from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.horario_repository import HorarioRepository

from app.application.use_cases.horario.consultar_disponibilidad import (
    ConsultarDisponibilidad
)

from app.presentation.api.schemas.horario import HorarioResponse

from app.presentation.api.dependencies import requerir_roles


router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"]
)


@router.get(
    "/",
    response_model=list[HorarioResponse]
)
def listar_horarios(
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "recepcionista",
            "fisioterapeuta"
        )
    )
):
    return ConsultarDisponibilidad(
        HorarioRepository(db)
    ).todos()


@router.get(
    "/disponibles",
    response_model=list[HorarioResponse]
)
def listar_disponibles(
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "recepcionista",
            "fisioterapeuta",
            "paciente"
        )
    )
):
    return ConsultarDisponibilidad(
        HorarioRepository(db)
    ).disponibles()