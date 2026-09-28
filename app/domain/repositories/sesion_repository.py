from abc import ABC, abstractmethod


class SesionRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_tratamiento(self, id_tratamiento):
        pass

    @abstractmethod
    def create(self, sesion):
        pass

    @abstractmethod
    def update(self, id, sesion):
        pass