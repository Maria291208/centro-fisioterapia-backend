from fastapi import HTTPException

from app.infrastructure.database.repositories.sesion_repository import SesionRepositoryImpl


class ConsultarSesiones:

    def __init__(self, repository):
        self.repository = repository

    def todas(self):
        return self.repository.get_all()

    def por_id(self, sesion_id: int):

        sesion = self.repository.get_by_id(
            sesion_id
        )

        if not sesion:
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )

        return sesion

    def por_tratamiento(self, tratamiento_id: int):
        return self.repository.get_by_tratamiento(
            tratamiento_id
        )

    def por_paciente(self, paciente_id: int):
        return self.repository.get_by_paciente(
            paciente_id
        )