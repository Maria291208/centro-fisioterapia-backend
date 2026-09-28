from abc import ABC, abstractmethod


class CitaRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, cita_id: int):
        pass

    @abstractmethod
    def get_by_paciente(self, paciente_id: int):
        pass

    @abstractmethod
    def get_by_fisioterapeuta(self, fisioterapeuta_id: int):
        pass

    @abstractmethod
    def create(self, cita):
        pass

    @abstractmethod
    def update(self, cita_id: int, datos: dict):
        pass