from app.infrastructure.database.models.asistencia import Asistencia


class AsistenciaRepositoryImpl:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.query(Asistencia).all()

    def get_by_id(self, id):
        return self.db.query(Asistencia).filter(
            Asistencia.id == id
        ).first()

    def get_by_sesion(self, id_sesion):
        return self.db.query(Asistencia).filter(
            Asistencia.id_sesion == id_sesion
        ).first()

    def create(self, asistencia):
        nuevo = Asistencia(
            fecha_registro=asistencia.fecha_registro,
            estado=asistencia.estado,
            observaciones=asistencia.observaciones,
            id_sesion=asistencia.id_sesion
        )

        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)

        return nuevo