from sqlalchemy.orm import Session

from app.infrastructure.database.models.reporte import Reporte


class ReporteRepositoryImpl:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Reporte).order_by(
        Reporte.id.desc()
    ).all()

    def get_by_id(self, reporte_id: int):
        return self.db.query(Reporte).filter(
            Reporte.id == reporte_id
        ).first()

    def create(self, reporte):

        nuevo = Reporte(
            fecha_generacion=reporte.fecha_generacion,
            periodo=reporte.periodo,
            porcentaje_cumplimiento=reporte.porcentaje_cumplimiento,
            id_tratamiento=reporte.id_tratamiento
        )

        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)

        return nuevo


ReporteRepository = ReporteRepositoryImpl