from app.infrastructure.database.models.evolucion import Evolucion


class EvolucionRepositoryImpl:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.query(Evolucion).all()

    def get_by_id(self, id):
        return self.db.query(Evolucion).filter(
            Evolucion.id == id
        ).first()

    def get_by_sesion(self, id_sesion):
        return self.db.query(Evolucion).filter(
            Evolucion.id_sesion == id_sesion
        ).first()

    def create(self, evolucion):
        nuevo = Evolucion(
            fecha=evolucion.fecha,
            descripcion=evolucion.descripcion,
            observaciones=evolucion.observaciones,
            id_sesion=evolucion.id_sesion
        )

        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)

        return nuevo