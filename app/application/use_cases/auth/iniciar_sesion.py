from fastapi import HTTPException

from app.infrastructure.database.repositories.usuario_repository import UsuarioRepository

from app.infrastructure.database.security import (
    verificar_password,
    crear_token
)


class IniciarSesion:

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def ejecutar(self, username: str, password: str):

        usuario = self.repository.get_by_username(username)

        if not usuario or not verificar_password(
            password,
            usuario.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas"
            )

        if not usuario.active:
            raise HTTPException(
                status_code=403,
                detail="Usuario inactivo"
            )

        token = crear_token({
         "sub": usuario.username,
         "id": usuario.id,
         "rol": usuario.rol,
         "id_paciente": usuario.id_paciente
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }