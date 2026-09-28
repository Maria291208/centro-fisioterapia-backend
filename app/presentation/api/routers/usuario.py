from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.usuario_repository import UsuarioRepository

from app.application.use_cases.auth.registrar_usuario import RegistrarUsuario
from app.application.use_cases.auth.iniciar_sesion import IniciarSesion

from app.presentation.api.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    Token
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


def get_registrar_usuario(
    db: Session = Depends(get_db)
):
    return RegistrarUsuario(
        UsuarioRepository(db)
    )


def get_iniciar_sesion(
    db: Session = Depends(get_db)
):
    return IniciarSesion(
        UsuarioRepository(db)
    )


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=201
)
def registrar(
    datos: UsuarioCreate,
    use_case: RegistrarUsuario = Depends(get_registrar_usuario)
):
    return use_case.ejecutar(datos)


@router.post(
    "/login",
    response_model=Token
)
def login(
    datos: OAuth2PasswordRequestForm = Depends(),
    use_case: IniciarSesion = Depends(get_iniciar_sesion)
):
    return use_case.ejecutar(
        datos.username,
        datos.password
    )