from fastapi import HTTPException

from app.infrastructure.database.repositories.paciente_repository import PacienteRepository
from app.presentation.api.schemas.paciente import PacienteUpdate


class ActualizarPaciente:

    def __init__(self, repository: PacienteRepository):
        self.repository = repository

    def ejecutar(
        self,
        paciente_id: int,
        datos: PacienteUpdate
    ):

        paciente = self.repository.get_by_id(paciente_id)

        if not paciente:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        datos_dict = datos.model_dump(exclude_unset=True)

        return self.repository.update(
            paciente_id,
            datos_dict
        )