from sqlalchemy.orm import Session

from app.domain.repositories.usuario_repository import (
    UsuarioRepository as UsuarioRepositoryContract
)

from app.infrastructure.database.models.usuario import Usuario


class UsuarioRepository(UsuarioRepositoryContract):

    def __init__(self, db: Session):

        self.db = db

    # ==========================================================
    # BUSCAR POR USERNAME
    # ==========================================================

    def get_by_username(
        self,
        username: str
    ):

        return (
            self.db
            .query(Usuario)
            .filter(
                Usuario.username == username
            )
            .first()
        )

    # ==========================================================
    # BUSCAR POR ID
    # ==========================================================

    def get_by_id(
        self,
        usuario_id: int
    ):

        return (
            self.db
            .query(Usuario)
            .filter(
                Usuario.id == usuario_id
            )
            .first()
        )

    # ==========================================================
    # OBTENER TODOS
    # ÚLTIMO REGISTRADO PRIMERO
    # ==========================================================

    def get_all(self):

        return (
            self.db
            .query(Usuario)
            .order_by(
                Usuario.id.desc()
            )
            .all()
        )

    # ==========================================================
    # OBTENER POR ROL
    # ==========================================================

    def get_by_rol(
        self,
        rol: str
    ):

        return (
            self.db
            .query(Usuario)
            .filter(
                Usuario.rol == rol
            )
            .order_by(
                Usuario.id.desc()
            )
            .all()
        )

    # ==========================================================
    # CREAR
    # ==========================================================

    def create(
        self,
        usuario_data: dict
    ):

        nuevo_usuario = Usuario(
            **usuario_data
        )

        self.db.add(
            nuevo_usuario
        )

        self.db.commit()

        self.db.refresh(
            nuevo_usuario
        )

        return nuevo_usuario

    # ==========================================================
    # ACTIVAR / DESACTIVAR
    # ==========================================================

    def update_active(
        self,
        usuario_id: int,
        active: bool
    ):

        usuario = self.get_by_id(
            usuario_id
        )

        if not usuario:

            return None

        usuario.active = active

        self.db.commit()

        self.db.refresh(
            usuario
        )

        return usuario