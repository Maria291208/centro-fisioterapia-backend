from sqlalchemy.orm import Session

from app.infrastructure.database.models.tratamiento import Tratamiento


class TratamientoRepositoryImpl:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.query(Tratamiento).all()

    def get_by_id(self, id):
        return self.db.query(Tratamiento).filter(
            Tratamiento.id == id
        ).first()

    def get_by_evaluacion(self, id_evaluacion):
        return self.db.query(Tratamiento).filter(
            Tratamiento.id_evaluacion == id_evaluacion
        ).first()

    def create(self, tratamiento):

        nuevo = Tratamiento(
            fecha_inicio=tratamiento.fecha_inicio,
            fecha_fin=tratamiento.fecha_fin,
            objetivo=tratamiento.objetivo,
            estado=tratamiento.estado,
            id_evaluacion=tratamiento.id_evaluacion
        )

        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)

        return nuevo

    def update(self, id, tratamiento):

        existente = self.get_by_id(id)

        if existente:

            existente.fecha_inicio = tratamiento.fecha_inicio
            existente.fecha_fin = tratamiento.fecha_fin
            existente.objetivo = tratamiento.objetivo
            existente.estado = tratamiento.estado

            self.db.commit()
            self.db.refresh(existente)

        return existente