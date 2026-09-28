from fastapi import HTTPException

from app.infrastructure.database.repositories.paciente_repository import PacienteRepository


class EliminarPaciente:

    def __init__(self, repository: PacienteRepository):
        self.repository = repository

    def ejecutar(self, paciente_id: int):

        paciente = self.repository.get_by_id(paciente_id)

        if not paciente:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        return self.repository.delete(paciente_id)