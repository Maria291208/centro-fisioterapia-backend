from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.infrastructure.database.repositories.cita_repository import CitaRepository
from app.infrastructure.database.repositories.horario_repository import HorarioRepository
from app.infrastructure.database.repositories.paciente_repository import PacienteRepository
from app.infrastructure.database.repositories.usuario_repository import UsuarioRepository

from app.application.use_cases.cita.registrar_cita import RegistrarCita
from app.application.use_cases.cita.consultar_citas import ConsultarCitas
from app.application.use_cases.cita.modificar_cita import ModificarCita

from app.presentation.api.schemas.cita import (
    CitaCreate,
    CitaUpdate,
    CitaResponse
)

from app.presentation.api.dependencies import requerir_roles
from app.infrastructure.database.repositories.sesion_repository import SesionRepositoryImpl
router = APIRouter(
    prefix="/citas",
    tags=["Citas"]
)

@router.post(
    "/",
    response_model=CitaResponse,
    status_code=201
)
def registrar_cita(
    datos: CitaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "recepcionista",
            "paciente"
        )
    )
):
    return RegistrarCita(
    CitaRepository(db),
    HorarioRepository(db),
    PacienteRepository(db),
    UsuarioRepository(db),
    SesionRepositoryImpl(db)
).ejecutar(datos)

@router.get(
    "/",
    response_model=list[CitaResponse]
)
def listar_citas(
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "recepcionista"
        )
    )
):

    return ConsultarCitas(
        CitaRepository(db)
    ).todas()

@router.get(
    "/paciente/{paciente_id}",
    response_model=list[CitaResponse]
)
def listar_citas_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "recepcionista",
            "paciente"
        )
    )
):
    if (
        usuario.rol == "paciente"
        and usuario.id_paciente != paciente_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Solo puede consultar sus propias citas"
        )
    return ConsultarCitas(
        CitaRepository(db)
    ).por_paciente(paciente_id)


@router.get(
    "/fisioterapeuta/{fisioterapeuta_id}",
    response_model=list[CitaResponse]
)
def listar_citas_fisioterapeuta(
    fisioterapeuta_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "recepcionista",
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
            detail="Solo puede consultar sus propias citas"
        )

    return ConsultarCitas(
        CitaRepository(db)
    ).por_fisioterapeuta(
        fisioterapeuta_id
    )

@router.get(
    "/{cita_id}",
    response_model=CitaResponse
)
def obtener_cita(
    cita_id: int,
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
    cita = ConsultarCitas(
        CitaRepository(db)
    ).por_id(cita_id)
    if (
        usuario.rol == "paciente"
        and usuario.id_paciente != cita.id_paciente
    ):
        raise HTTPException(
            status_code=403,
            detail="Solo puede consultar sus propias citas"
        )
    if (
        usuario.rol == "fisioterapeuta"
        and usuario.id != cita.id_fisioterapeuta
    ):
        raise HTTPException(
            status_code=403,
            detail="Solo puede consultar sus propias citas"
        )

    return cita
@router.put(
    "/{cita_id}",
    response_model=CitaResponse
)
def modificar_cita(
    cita_id: int,
    datos: CitaUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "recepcionista",
            "paciente"
        )
    )
):

    cita = ConsultarCitas(
        CitaRepository(db)
    ).por_id(cita_id)
    if (
        usuario.rol == "paciente"
        and usuario.id_paciente != cita.id_paciente
    ):
        raise HTTPException(
            status_code=403,
            detail="Solo puede modificar sus propias citas"
        )

    return ModificarCita(
    CitaRepository(db),
    SesionRepositoryImpl(db)
).ejecutar(
    cita_id,
    datos
)