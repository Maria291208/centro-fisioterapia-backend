from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.infrastructure.database.security import decodificar_token
from app.infrastructure.database.repositories.usuario_repository import UsuarioRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="usuarios/login"
)


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decodificar_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

    username = payload.get("sub")

    usuario = UsuarioRepository(db).get_by_username(username)

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    # NUEVO: verificar si la cuenta está activa
    if not usuario.active:
        raise HTTPException(
            status_code=403,
            detail="Usuario inactivo"
        )

    return usuario


def requerir_roles(*roles_permitidos: str):

    def verificar(
        usuario=Depends(obtener_usuario_actual)
    ):

        if usuario.rol not in roles_permitidos:
            raise HTTPException(
                status_code=403,
                detail="No tiene permisos para esta acción"
            )

        return usuario

    return verificar