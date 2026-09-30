from sqlalchemy.orm import Session

from app.infrastructure.database.models.sesion import Sesion
from app.infrastructure.database.models.tratamiento import Tratamiento
from app.infrastructure.database.models.evaluacion import Evaluacion
from app.infrastructure.database.models.cita import Cita


class SesionRepositoryImpl:

    def __init__(self, db: Session):
        self.db = db

    
    def get_all(self):

     return (
        self.db.query(Sesion)
        .order_by(Sesion.id.desc())
        .all()
    )



    def get_by_id(self, id):

        return (
            self.db.query(Sesion)
            .filter(
                Sesion.id == id
            )
            .first()
        )

  

    def get_by_tratamiento(
        self,
        id_tratamiento
    ):

        return (
            self.db.query(Sesion)
            .filter(
                Sesion.id_tratamiento ==
                id_tratamiento
            )
            .order_by(
                Sesion.numero_sesion
            )
            .all()
        )

   
    def get_by_tratamiento_fecha(
        self,
        id_tratamiento,
        fecha
    ):

        return (
            self.db.query(Sesion)
            .filter(
                Sesion.id_tratamiento ==
                id_tratamiento,
                Sesion.fecha == fecha
            )
            .first()
        )


    def get_by_tratamiento_numero(
        self,
        id_tratamiento,
        numero_sesion
    ):

        return (
            self.db.query(Sesion)
            .filter(
                Sesion.id_tratamiento ==
                id_tratamiento,
                Sesion.numero_sesion ==
                numero_sesion
            )
            .first()
        )


    def get_by_fisioterapeuta_fecha_horario(
        self,
        id_fisioterapeuta,
        fecha,
        id_horario,
        excluir_sesion_id=None
    ):

        consulta = (
            self.db.query(Sesion)
            .join(
                Tratamiento,
                Sesion.id_tratamiento ==
                Tratamiento.id
            )
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
                id_fisioterapeuta,
                Sesion.fecha == fecha,
                Sesion.id_horario ==
                id_horario
            )
        )

        if excluir_sesion_id is not None:

            consulta = consulta.filter(
                Sesion.id !=
                excluir_sesion_id
            )

        return consulta.first()

    def get_by_paciente_fecha_horario(
        self,
        id_paciente,
        fecha,
        id_horario,
        excluir_sesion_id=None
    ):

        consulta = (
            self.db.query(Sesion)
            .join(
                Tratamiento,
                Sesion.id_tratamiento ==
                Tratamiento.id
            )
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
                Cita.id_paciente ==
                id_paciente,
                Sesion.fecha == fecha,
                Sesion.id_horario ==
                id_horario
            )
        )

        if excluir_sesion_id is not None:

            consulta = consulta.filter(
                Sesion.id !=
                excluir_sesion_id
            )

        return consulta.first()

 
    def get_by_fisioterapeuta(
        self,
        id_fisioterapeuta
    ):

        return (
            self.db.query(Sesion)
            .join(
                Tratamiento,
                Sesion.id_tratamiento ==
                Tratamiento.id
            )
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
                Sesion.id.desc()
            )
            .all()
        )

 
    def get_by_paciente(
    self,
    id_paciente
):

     return (
        self.db.query(Sesion)
        .join(
            Tratamiento,
            Sesion.id_tratamiento ==
            Tratamiento.id
        )
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
            Cita.id_paciente ==
            id_paciente
        )
        .order_by(
            Sesion.id.desc()
        )
        .all()
    )


    def create(self, sesion):

        nuevo = Sesion(

            fecha=sesion.fecha,

            numero_sesion=
                sesion.numero_sesion,

            estado=
                sesion.estado,

            motivo_reprogramacion=
                sesion.motivo_reprogramacion,

            id_tratamiento=
                sesion.id_tratamiento,

            id_horario=
                sesion.id_horario
        )

        self.db.add(nuevo)

        self.db.commit()

        self.db.refresh(nuevo)

        return nuevo

    def update(
        self,
        id,
        sesion
    ):

        existente = self.get_by_id(id)

        if not existente:
            return None

        existente.fecha = sesion.fecha

        existente.numero_sesion = (
            sesion.numero_sesion
        )

        existente.estado = (
            sesion.estado
        )

        existente.motivo_reprogramacion = (
            sesion.motivo_reprogramacion
        )

        existente.id_tratamiento = (
            sesion.id_tratamiento
        )

        existente.id_horario = (
            sesion.id_horario
        )

        self.db.commit()

        self.db.refresh(existente)

        return existente