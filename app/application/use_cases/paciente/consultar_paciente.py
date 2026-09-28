from fastapi import HTTPException

from app.infrastructure.database.repositories.paciente_repository import PacienteRepository


class ConsultarPaciente:

    def __init__(self, repository: PacienteRepository):
        self.repository = repository

    def todos(self):
        return self.repository.get_all()

    def por_id(self, paciente_id: int):

        paciente = self.repository.get_by_id(paciente_id)

        if not paciente:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        return paciente