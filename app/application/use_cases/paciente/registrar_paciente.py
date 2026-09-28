from app.domain.entities.paciente import Paciente
from app.infrastructure.database.security import hashear_password


class RegistrarPaciente:

    def __init__(self, paciente_repo, usuario_repo):
        self.paciente_repo = paciente_repo
        self.usuario_repo = usuario_repo

    def ejecutar(self, datos):

        paciente = Paciente(
            nombre=datos.nombre,
            apellido=datos.apellido,
            ci=datos.ci,
            telefono=datos.telefono,
            direccion=datos.direccion,
            fecha_nacimiento=datos.fecha_nacimiento
        )

        paciente_creado = self.paciente_repo.create(paciente)

        usuario = {
            "username": datos.username,
            "password_hash": hashear_password(datos.password),
            "rol": "paciente",
            "active": True,
            "id_paciente": paciente_creado.id
        }

        self.usuario_repo.create(usuario)

        return paciente_creado