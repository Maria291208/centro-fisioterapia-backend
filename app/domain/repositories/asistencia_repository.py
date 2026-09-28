from abc import ABC, abstractmethod


class AsistenciaRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_sesion(self, id_sesion):
        pass

    @abstractmethod
    def create(self, asistencia):
        pass