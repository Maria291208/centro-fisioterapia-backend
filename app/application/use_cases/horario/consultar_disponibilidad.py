from app.infrastructure.database.repositories.horario_repository import HorarioRepository


class ConsultarDisponibilidad:

    def __init__(self, repository: HorarioRepository):
        self.repository = repository

    def todos(self):
        return self.repository.get_all()

    def disponibles(self):
        return self.repository.get_disponibles()