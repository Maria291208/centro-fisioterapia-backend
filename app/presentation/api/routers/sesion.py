from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db

from app.infrastructure.database.repositories.sesion_repository import (
    SesionRepositoryImpl
)

from app.infrastructure.database.repositories.tratamiento_repository import (
    TratamientoRepositoryImpl
)

from app.infrastructure.database.repositories.horario_repository import (
    HorarioRepositoryImpl
)

from app.infrastructure.database.repositories.evaluacion_repository import (
    EvaluacionRepositoryImpl
)

from app.infrastructure.database.repositories.cita_repository import (
    CitaRepository
)

from app.application.use_cases.tratamiento.programar_sesiones import (
    ProgramarSesion
)

from app.application.use_cases.sesion.consultar_sesiones import (
    ConsultarSesiones
)

from app.application.use_cases.sesion.reprogramar_sesion import (
    ReprogramarSesion
)

from app.presentation.api.schemas.sesion import (
    SesionCreate,
    SesionReprogramar,
    SesionResponse
)

from app.presentation.api.dependencies import requerir_roles


router = APIRouter(
    prefix="/sesiones",
    tags=["Sesiones"]
)


# ============================================================
# PROGRAMAR SESIÓN
# ============================================================

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


# ============================================================
# LISTAR TODAS LAS SESIONES
# ============================================================

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


# ============================================================
# LISTAR SESIONES DE UN PACIENTE
# ============================================================
@router.get(
    "/fisioterapeuta/{fisioterapeuta_id}",
    response_model=list[SesionResponse]
)
def listar_sesiones_fisioterapeuta(
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
            detail="Solo puede consultar sus propias sesiones"
        )

    repo = SesionRepositoryImpl(db)

    return repo.get_by_fisioterapeuta(
        fisioterapeuta_id
    )
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

    return caso.por_paciente(
        paciente_id
    )


# ============================================================
# LISTAR SESIONES DE UN TRATAMIENTO
# ============================================================

@router.get(
    "/tratamiento/{tratamiento_id}",
    response_model=list[SesionResponse]
)
def listar_sesiones_tratamiento(
    tratamiento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "fisioterapeuta"
        )
    )
):

    repo = SesionRepositoryImpl(db)

    return repo.get_by_tratamiento(
        tratamiento_id
    )

@router.get(
    "/fisioterapeuta/{fisioterapeuta_id}",
    response_model=list[SesionResponse]
)
def listar_sesiones_fisioterapeuta(
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
            detail="No puede consultar sesiones de otro fisioterapeuta"
        )

    repo = SesionRepositoryImpl(db)

    return repo.get_by_fisioterapeuta(
        fisioterapeuta_id
    )
# ============================================================
# REPROGRAMAR SESIÓN
# ============================================================
@router.put(
    "/{sesion_id}/reprogramar",
    response_model=SesionResponse
)
def reprogramar_sesion(
    sesion_id: int,
    datos: SesionReprogramar,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "recepcionista",
            "paciente",
            "fisioterapeuta"
        )
    )
):

    sesion_repo = SesionRepositoryImpl(db)
    tratamiento_repo = TratamientoRepositoryImpl(db)
    evaluacion_repo = EvaluacionRepositoryImpl(db)
    cita_repo = CitaRepository(db)
    horario_repo = HorarioRepositoryImpl(db)

    sesion = sesion_repo.get_by_id(sesion_id)

    if not sesion:
        raise HTTPException(
            status_code=404,
            detail="La sesión no existe"
        )

    tratamiento = tratamiento_repo.get_by_id(
        sesion.id_tratamiento
    )

    if not tratamiento:
        raise HTTPException(
            status_code=404,
            detail="El tratamiento no existe"
        )

    evaluacion = evaluacion_repo.get_by_id(
        tratamiento.id_evaluacion
    )

    if not evaluacion:
        raise HTTPException(
            status_code=404,
            detail="La evaluación no existe"
        )

    cita = cita_repo.get_by_id(
        evaluacion.id_cita
    )

    if not cita:
        raise HTTPException(
            status_code=404,
            detail="La cita no existe"
        )

    # PACIENTE: solamente sus propias sesiones
    if (
        usuario.rol == "paciente"
        and usuario.id_paciente != cita.id_paciente
    ):
        raise HTTPException(
            status_code=403,
            detail="No puede reprogramar esta sesión"
        )

    # FISIOTERAPEUTA: solamente sus sesiones
    if (
        usuario.rol == "fisioterapeuta"
        and usuario.id != cita.id_fisioterapeuta
    ):
        raise HTTPException(
            status_code=403,
            detail="No puede reprogramar esta sesión"
        )

    use_case = ReprogramarSesion(
        sesion_repo,
        tratamiento_repo,
        evaluacion_repo,
        cita_repo,
        horario_repo
    )

    return use_case.ejecutar(
        sesion_id,
        datos
    )