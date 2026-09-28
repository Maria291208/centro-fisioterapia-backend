from abc import ABC, abstractmethod


class EvolucionRepository(ABC):

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
    def create(self, evolucion):
        pass

    @abstractmethod
    def update(self, id, evolucion):
        pass