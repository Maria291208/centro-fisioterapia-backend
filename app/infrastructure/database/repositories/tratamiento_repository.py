from sqlalchemy.orm import Session

from app.infrastructure.database.models.tratamiento import Tratamiento
from app.infrastructure.database.models.evaluacion import Evaluacion
from app.infrastructure.database.models.cita import Cita


class TratamientoRepositoryImpl:

    def __init__(self, db: Session):
        self.db = db


    def get_all(self):

        return (
        self.db.query(Tratamiento)
        .order_by(
            Tratamiento.id.desc()
        )
        .all()
    )



    def get_by_id(self, id):

        return (
            self.db.query(Tratamiento)
            .filter(
                Tratamiento.id == id
            )
            .first()
        )

 
    def get_by_evaluacion(
        self,
        id_evaluacion
    ):

        return (
            self.db.query(Tratamiento)
            .filter(
                Tratamiento.id_evaluacion ==
                id_evaluacion
            )
            .first()
        )


    def get_by_fisioterapeuta(
        self,
        id_fisioterapeuta
    ):

        return (
            self.db.query(Tratamiento)

            .join(
                Evaluacion,
                Tratamiento.id_evaluacion ==
                Evaluacion.id
            )

            .join(
                Cita,
                Evaluacion.id_cita ==
                Cita.id
            )

            .filter(
                Cita.id_fisioterapeuta ==
                id_fisioterapeuta
            )

            .order_by(
                Tratamiento.id.desc()
            )

            .all()
        )

    def create(
        self,
        tratamiento
    ):

        nuevo = Tratamiento(

            fecha_inicio=
                tratamiento.fecha_inicio,

            fecha_fin=
                tratamiento.fecha_fin,

            objetivo=
                tratamiento.objetivo,

            numero_sesiones=
                tratamiento.numero_sesiones,

            estado=
                tratamiento.estado,

            id_evaluacion=
                tratamiento.id_evaluacion
        )

        self.db.add(nuevo)

        self.db.commit()

        self.db.refresh(nuevo)

        return nuevo


    def update(
        self,
        id,
        tratamiento
    ):

        existente = self.get_by_id(id)

        if not existente:
            return None

        existente.fecha_inicio = (
            tratamiento.fecha_inicio
        )

        existente.fecha_fin = (
            tratamiento.fecha_fin
        )

        existente.objetivo = (
            tratamiento.objetivo
        )

        existente.numero_sesiones = (
            tratamiento.numero_sesiones
        )

        existente.estado = (
            tratamiento.estado
        )

        self.db.commit()

        self.db.refresh(existente)

        return existente