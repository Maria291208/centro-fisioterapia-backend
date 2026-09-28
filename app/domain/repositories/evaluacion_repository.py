from abc import ABC, abstractmethod


class EvaluacionRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, evaluacion_id: int):
        pass

    @abstractmethod
    def get_by_cita(self, cita_id: int):
        pass

    @abstractmethod
    def create(self, evaluacion):
        pass

    @abstractmethod
    def update(self, evaluacion_id: int, datos: dict):
        pass