from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.infrastructure.database.repositories.sesion_repository import SesionRepositoryImpl
from app.infrastructure.database.repositories.tratamiento_repository import TratamientoRepositoryImpl
from app.infrastructure.database.repositories.horario_repository import HorarioRepositoryImpl

from app.application.use_cases.tratamiento.programar_sesiones import ProgramarSesion

from app.application.use_cases.sesion.consultar_sesiones import ConsultarSesiones

from app.presentation.api.schemas.sesion import (
    SesionCreate,
    SesionResponse
)

from app.presentation.api.dependencies import requerir_roles


router = APIRouter(
    prefix="/sesiones",
    tags=["Sesiones"]
)


# ==========================================
# PROGRAMAR SESIÓN
# ==========================================

@router.post(
    "/",
    response_model=SesionResponse
)
def programar_sesion(
    datos: SesionCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "fisioterapeuta"
        )
    )
):

    sesion_repo = SesionRepositoryImpl(db)

    tratamiento_repo = TratamientoRepositoryImpl(db)

    horario_repo = HorarioRepositoryImpl(db)

    caso = ProgramarSesion(
        sesion_repo,
        tratamiento_repo,
        horario_repo
    )

    return caso.ejecutar(datos)


# ==========================================
# LISTAR TODAS LAS SESIONES
# ==========================================

@router.get(
    "/",
    response_model=list[SesionResponse]
)
def listar_sesiones(
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "fisioterapeuta"
        )
    )
):

    repo = SesionRepositoryImpl(db)

    return repo.get_all()


# ==========================================
# LISTAR SESIONES DE UN PACIENTE
# ==========================================

@router.get(
    "/paciente/{paciente_id}",
    response_model=list[SesionResponse]
)
def listar_sesiones_paciente(
    paciente_id: int,
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

    # El paciente solamente puede
    # consultar sus propias sesiones
    if (
        usuario.rol == "paciente"
        and usuario.id_paciente != paciente_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Solo puede consultar sus propias sesiones"
        )

    caso = ConsultarSesiones(
        SesionRepositoryImpl(db)
    )

    return caso.por_paciente(paciente_id)