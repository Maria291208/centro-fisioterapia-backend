from abc import ABC, abstractmethod


class HorarioRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, horario_id: int):
        pass

    @abstractmethod
    def get_disponibles(self):
        pass

    @abstractmethod
    def create(self, horario):
        pass

    @abstractmethod
    def update(self, horario_id: int, datos: dict):
        pass

    @abstractmethod
    def delete(self, horario_id: int):
        pass