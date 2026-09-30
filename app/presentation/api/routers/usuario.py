from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session


from app.infrastructure.database.database import (
    get_db
)


from app.infrastructure.database.repositories.usuario_repository import (
    UsuarioRepository
)


from app.application.use_cases.auth.registrar_usuario import (
    RegistrarUsuario
)


from app.application.use_cases.auth.iniciar_sesion import (
    IniciarSesion
)


from app.presentation.api.dependencies import (
    requerir_roles
)


from app.presentation.api.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    Token,
    UsuarioEstadoUpdate
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


# ==========================================================
# DEPENDENCY REGISTRAR USUARIO
# ==========================================================

def get_registrar_usuario(
    db: Session = Depends(get_db)
):

    return RegistrarUsuario(
        UsuarioRepository(db)
    )


# ==========================================================
# DEPENDENCY LOGIN
# ==========================================================

def get_iniciar_sesion(
    db: Session = Depends(get_db)
):

    return IniciarSesion(
        UsuarioRepository(db)
    )


# ==========================================================
# REGISTRAR USUARIO
# ==========================================================

@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=201
)
def registrar(
    datos: UsuarioCreate,
    use_case: RegistrarUsuario = Depends(
        get_registrar_usuario
    )
):

    return use_case.ejecutar(
        datos
    )


# ==========================================================
# LOGIN
# ==========================================================

@router.post(
    "/login",
    response_model=Token
)
def login(
    datos: OAuth2PasswordRequestForm = Depends(),
    use_case: IniciarSesion = Depends(
        get_iniciar_sesion
    )
):

    return use_case.ejecutar(
        datos.username,
        datos.password
    )


# ==========================================================
# LISTAR TODOS LOS USUARIOS
# SOLO ADMINISTRADOR
# ==========================================================

@router.get(
    "/",
    response_model=list[UsuarioResponse]
)
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador"
        )
    )
):

    return (
        UsuarioRepository(db)
        .get_all()
    )


# ==========================================================
# LISTAR FISIOTERAPEUTAS
# ADMINISTRADOR Y RECEPCIONISTA
# ==========================================================

@router.get("/fisioterapeutas", response_model=list[UsuarioResponse])
def listar_fisioterapeutas(
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador",
            "recepcionista",
            "paciente"
        )
    )
):
    return UsuarioRepository(db).get_by_rol("fisioterapeuta")


# ==========================================================
# CREAR USUARIO DESDE ADMINISTRADOR
# ==========================================================

@router.post(
    "/admin/crear",
    response_model=UsuarioResponse,
    status_code=201
)
def crear_usuario_admin(
    datos: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador"
        )
    )
):

    # ------------------------------------------------------
    # EL ADMINISTRADOR SOLO PUEDE CREAR PERSONAL
    # ------------------------------------------------------

    if datos.rol not in [
        "recepcionista",
        "fisioterapeuta"
    ]:

        raise HTTPException(
            status_code=400,
            detail=(
                "El administrador solo puede "
                "crear usuarios recepcionista "
                "o fisioterapeuta"
            )
        )

    use_case = RegistrarUsuario(
        UsuarioRepository(db)
    )

    return use_case.ejecutar(
        datos
    )


# ==========================================================
# ACTIVAR / DESACTIVAR USUARIO
# SOLO ADMINISTRADOR
# ==========================================================

@router.put(
    "/{usuario_id}/estado",
    response_model=UsuarioResponse
)
def cambiar_estado_usuario(
    usuario_id: int,
    datos: UsuarioEstadoUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(
        requerir_roles(
            "administrador"
        )
    )
):

    # ------------------------------------------------------
    # NO PERMITIR QUE EL ADMIN SE DESACTIVE A SÍ MISMO
    # ------------------------------------------------------

    if usuario.id == usuario_id:

        raise HTTPException(
            status_code=400,
            detail=(
                "El administrador no puede "
                "desactivar su propia cuenta"
            )
        )

    usuario_actualizado = (
        UsuarioRepository(db)
        .update_active(
            usuario_id,
            datos.active
        )
    )

    if not usuario_actualizado:

        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario_actualizado