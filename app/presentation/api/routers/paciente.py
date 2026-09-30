from http.client import HTTPException

from app.infrastructure.database.models.cita import Cita
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.infrastructure.database.repositories.paciente_repository import PacienteRepository
from app.infrastructure.database.repositories.usuario_repository import UsuarioRepository

from app.application.use_cases.paciente.registrar_paciente import RegistrarPaciente
from app.application.use_cases.paciente.consultar_paciente import ConsultarPaciente
from app.application.use_cases.paciente.actualizar_paciente import ActualizarPaciente
from app.application.use_cases.paciente.eliminar_paciente import EliminarPaciente

from app.presentation.api.schemas.paciente import (
    PacienteCreate,
    PacienteUpdate,
    PacienteResponse
)

from app.presentation.api.dependencies import requerir_roles


router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)


# PACIENTE SE REGISTRA SOLO
@router.post(
    "/registro",
    response_model=PacienteResponse,
    status_code=201
)
def registro_paciente(
    datos: PacienteCreate,
    db: Session = Depends(get_db)
):
    return RegistrarPaciente(
        PacienteRepository(db),
        UsuarioRepository(db)
    ).ejecutar(datos)


# RECEPCIONISTA O ADMINISTRADOR REGISTRAN PACIENTE
@router.post(
    "/",
    response_model=PacienteResponse,
    status_code=201
)
def registrar_paciente(
    datos: PacienteCreate,
    db: Session = Depends(get_db),
    usuario=Depends(requerir_roles("administrador", "recepcionista"))
):
    return RegistrarPaciente(
        PacienteRepository(db),
        UsuarioRepository(db)
    ).ejecutar(datos)

@router.get(
    "/",
    response_model=list[PacienteResponse]
)
def listar_pacientes(
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "recepcionista"
        )
    )
):
    return (
        PacienteRepository(db)
        .get_all()
    )
@router.get(
    "/{paciente_id}",
    response_model=PacienteResponse
)
def obtener_paciente(
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
    # El paciente solamente puede consultar su propio perfil
    if (
        usuario.rol == "paciente"
        and usuario.id_paciente != paciente_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Solo puede consultar su propio perfil"
        )

    # El fisioterapeuta solamente puede consultar
    # pacientes que tengan una cita asignada a él
    if usuario.rol == "fisioterapeuta":

        citas = (
            db.query(Cita)
            .filter(
                Cita.id_paciente == paciente_id,
                Cita.id_fisioterapeuta == usuario.id
            )
            .first()
        )

        if not citas:
            raise HTTPException(
                status_code=403,
                detail="No tiene acceso a este paciente"
            )

    return ConsultarPaciente(
        PacienteRepository(db)
    ).por_id(paciente_id)


@router.put(
    "/{paciente_id}",
    response_model=PacienteResponse
)
def actualizar_paciente(
    paciente_id: int,
    datos: PacienteUpdate,
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
            detail="Solo puede modificar su propio perfil"
        )

    return ActualizarPaciente(
        PacienteRepository(db)
    ).ejecutar(paciente_id, datos)


@router.delete(
    "/{paciente_id}",
    response_model=PacienteResponse
)
def eliminar_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(requerir_roles("administrador"))
):
    return EliminarPaciente(
        PacienteRepository(db)
    ).ejecutar(paciente_id)

@router.get(
    "/{paciente_id}",
    response_model=PacienteResponse
)
def obtener_paciente(
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
            detail="Solo puede consultar su propio perfil"
        )

    return ConsultarPaciente(
        PacienteRepository(db)
    ).por_id(paciente_id)