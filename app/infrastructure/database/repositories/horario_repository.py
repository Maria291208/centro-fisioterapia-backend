from sqlalchemy.orm import Session

from app.infrastructure.database.models.horario import Horario


class HorarioRepositoryImpl:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Horario).all()

    def get_by_id(self, id):
        return (
            self.db
            .query(Horario)
            .filter(Horario.id == id)
            .first()
        )

    def get_disponibles(self):
        return (
            self.db
            .query(Horario)
            .filter(Horario.estado == "disponible")
            .all()
        )

    def create(self, horario):
        nuevo = Horario(
            hora_inicio=horario.hora_inicio,
            hora_fin=horario.hora_fin,
            estado=horario.estado
        )

        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)

        return nuevo

    def update(self, id, horario):
        existente = self.get_by_id(id)

        if not existente:
            return None

        if isinstance(horario, dict):
            if "hora_inicio" in horario:
                existente.hora_inicio = horario["hora_inicio"]

            if "hora_fin" in horario:
                existente.hora_fin = horario["hora_fin"]

            if "estado" in horario:
                existente.estado = horario["estado"]

        else:
            existente.hora_inicio = horario.hora_inicio
            existente.hora_fin = horario.hora_fin
            existente.estado = horario.estado

        self.db.commit()
        self.db.refresh(existente)

        return existente

    def delete(self, id):
        existente = self.get_by_id(id)

        if existente:
            self.db.delete(existente)
            self.db.commit()

        return existente


HorarioRepository = HorarioRepositoryImpl