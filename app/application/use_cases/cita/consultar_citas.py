from fastapi import HTTPException

from app.infrastructure.database.repositories.cita_repository import CitaRepository


class ConsultarCitas:

    def __init__(self, repository: CitaRepository):
        self.repository = repository

    def todas(self):
        return self.repository.get_all()

    def por_id(self, cita_id: int):

        cita = self.repository.get_by_id(cita_id)

        if not cita:
            raise HTTPException(
                status_code=404,
                detail="Cita no encontrada"
            )

        return cita

    def por_paciente(self, paciente_id: int):
        return self.repository.get_by_paciente(paciente_id)

    def por_fisioterapeuta(self, fisioterapeuta_id: int):
        return self.repository.get_by_fisioterapeuta(
            fisioterapeuta_id
        )