from abc import ABC, abstractmethod


class TratamientoRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_evaluacion(self, id_evaluacion):
        pass

    @abstractmethod
    def create(self, tratamiento):
        pass

    @abstractmethod
    def update(self, id, tratamiento):
        pass