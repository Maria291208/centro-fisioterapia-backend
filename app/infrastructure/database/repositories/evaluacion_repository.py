from sqlalchemy.orm import Session

from app.infrastructure.database.models.evaluacion import Evaluacion


class EvaluacionRepositoryImpl:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Evaluacion).all()

    def get_by_id(self, id):
        return (
            self.db
            .query(Evaluacion)
            .filter(Evaluacion.id == id)
            .first()
        )

    def get_by_cita(self, id_cita):
        return (
            self.db
            .query(Evaluacion)
            .filter(Evaluacion.id_cita == id_cita)
            .first()
        )

    def create(self, evaluacion):
        if isinstance(evaluacion, dict):
            nueva = Evaluacion(
                fecha=evaluacion["fecha"],
                diagnostico=evaluacion["diagnostico"],
                id_cita=evaluacion["id_cita"]
            )
        else:
            nueva = Evaluacion(
                fecha=evaluacion.fecha,
                diagnostico=evaluacion.diagnostico,
                id_cita=evaluacion.id_cita
            )

        self.db.add(nueva)
        self.db.commit()
        self.db.refresh(nueva)

        return nueva

    def update(self, id, evaluacion):
        existente = self.get_by_id(id)

        if existente:
            if isinstance(evaluacion, dict):
                existente.fecha = evaluacion["fecha"]
                existente.diagnostico = evaluacion["diagnostico"]
            else:
                existente.fecha = evaluacion.fecha
                existente.diagnostico = evaluacion.diagnostico

            self.db.commit()
            self.db.refresh(existente)

        return existente


EvaluacionRepository = EvaluacionRepositoryImpl