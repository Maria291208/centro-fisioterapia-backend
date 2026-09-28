from sqlalchemy.orm import Session

from app.domain.repositories.usuario_repository import (
    UsuarioRepository as UsuarioRepositoryContract
)

from app.infrastructure.database.models.usuario import Usuario


class UsuarioRepository(UsuarioRepositoryContract):

    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str):
        return (
            self.db
            .query(Usuario)
            .filter(Usuario.username == username)
            .first()
        )

    def get_by_id(self, usuario_id: int):
        return (
            self.db
            .query(Usuario)
            .filter(Usuario.id == usuario_id)
            .first()
        )

    def create(self, usuario_data: dict):
        nuevo_usuario = Usuario(**usuario_data)

        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)

        return nuevo_usuario