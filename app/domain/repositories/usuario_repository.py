from abc import ABC, abstractmethod


class UsuarioRepository(ABC):

    @abstractmethod
    def get_by_username(self, username: str):
        pass

    @abstractmethod
    def get_by_id(self, usuario_id: int):
        pass

    @abstractmethod
    def create(self, usuario):
        pass