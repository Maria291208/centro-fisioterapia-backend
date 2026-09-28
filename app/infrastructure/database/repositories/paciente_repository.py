from sqlalchemy.orm import Session

from app.infrastructure.database.models.paciente import Paciente


class PacienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Paciente).all()

    def get_by_id(self, id):
        return (
            self.db
            .query(Paciente)
            .filter(Paciente.id == id)
            .first()
        )

    def get_by_ci(self, ci):
        return (
            self.db
            .query(Paciente)
            .filter(Paciente.ci == ci)
            .first()
        )

    def create(self, paciente):
        nuevo_paciente = Paciente(
            nombre=paciente.nombre,
            apellido=paciente.apellido,
            ci=paciente.ci,
            telefono=paciente.telefono,
            direccion=paciente.direccion,
            fecha_nacimiento=paciente.fecha_nacimiento
        )

        self.db.add(nuevo_paciente)
        self.db.commit()
        self.db.refresh(nuevo_paciente)

        return nuevo_paciente

    def update(self, id, paciente):
        existente = self.get_by_id(id)

        if existente:
            existente.nombre = paciente.nombre
            existente.apellido = paciente.apellido
            existente.ci = paciente.ci
            existente.telefono = paciente.telefono
            existente.direccion = paciente.direccion
            existente.fecha_nacimiento = paciente.fecha_nacimiento

            self.db.commit()
            self.db.refresh(existente)

        return existente

    def delete(self, id):
        existente = self.get_by_id(id)

        if existente:
            self.db.delete(existente)
            self.db.commit()

        return existente