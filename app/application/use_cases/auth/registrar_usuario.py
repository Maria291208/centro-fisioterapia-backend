from fastapi import HTTPException

from app.infrastructure.database.repositories.usuario_repository import (
    UsuarioRepository
)

from app.presentation.api.schemas.usuario import UsuarioCreate

from app.infrastructure.database.security import (
    hashear_password
)


class RegistrarUsuario:

    def __init__(
        self,
        usuario_repository: UsuarioRepository
    ):
        self.usuario_repository = usuario_repository

    def ejecutar(
        self,
        datos: UsuarioCreate
    ):

        # ======================================================
        # VERIFICAR SI EL USUARIO YA EXISTE
        # ======================================================

        existe = (
            self.usuario_repository
            .get_by_username(
                datos.username
            )
        )

        if existe:

            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )

        # ======================================================
        # ROLES VÁLIDOS
        # ======================================================

        roles_validos = [
            "paciente",
            "recepcionista",
            "fisioterapeuta",
            "administrador"
        ]

        if datos.rol not in roles_validos:

            raise HTTPException(
                status_code=400,
                detail="Rol no válido"
            )

        # ======================================================
        # CREAR USUARIO
        # ======================================================

        usuario_dict = {

            "username":
                datos.username,

            "password_hash":
                hashear_password(
                    datos.password
                ),

            "rol":
                datos.rol,

            "active":
                True
        }

        return (
            self.usuario_repository
            .create(usuario_dict)
        )