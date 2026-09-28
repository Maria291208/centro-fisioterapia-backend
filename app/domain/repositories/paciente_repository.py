from abc import ABC, abstractmethod


class PacienteRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, paciente_id: int):
        pass

    @abstractmethod
    def get_by_ci(self, ci: str):
        pass

    @abstractmethod
    def create(self, paciente):
        pass

    @abstractmethod
    def update(self, paciente_id: int, datos: dict):
        pass

    @abstractmethod
    def delete(self, paciente_id: int):
        pass