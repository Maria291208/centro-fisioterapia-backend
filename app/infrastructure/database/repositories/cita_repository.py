from sqlalchemy.orm import Session

from app.infrastructure.database.models.cita import Cita


class CitaRepository:

    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # TODAS LAS CITAS
    # ÚLTIMA REGISTRADA PRIMERO
    # ==========================================================

    def get_all(self):

        return (
            self.db.query(Cita)
            .order_by(Cita.id.desc())
            .all()
        )

    # ==========================================================
    # CITA POR ID
    # ==========================================================

    def get_by_id(self, id):

        return (
            self.db.query(Cita)
            .filter(
                Cita.id == id
            )
            .first()
        )

    # ==========================================================
    # CITAS DEL PACIENTE
    # ÚLTIMA REGISTRADA PRIMERO
    # ==========================================================

    def get_by_paciente(self, id_paciente):

        return (
            self.db.query(Cita)
            .filter(
                Cita.id_paciente == id_paciente
            )
            .order_by(Cita.id.desc())
            .all()
        )

    # ==========================================================
    # CITAS DEL FISIOTERAPEUTA
    # ÚLTIMA REGISTRADA PRIMERO
    # ==========================================================

    def get_by_fisioterapeuta(
        self,
        id_fisioterapeuta
    ):

        return (
            self.db.query(Cita)
            .filter(
                Cita.id_fisioterapeuta ==
                id_fisioterapeuta
            )
            .order_by(Cita.id.desc())
            .all()
        )

    # ==========================================================
    # CONFLICTO PACIENTE
    # ==========================================================

    def get_by_paciente_fecha_horario(
        self,
        id_paciente,
        fecha,
        id_horario
    ):

        return (
            self.db.query(Cita)
            .filter(
                Cita.id_paciente ==
                id_paciente,
                Cita.fecha == fecha,
                Cita.id_horario ==
                id_horario,
                Cita.estado ==
                "programada"
            )
            .first()
        )

    # ==========================================================
    # CONFLICTO FISIOTERAPEUTA
    # ==========================================================

    def get_by_fisioterapeuta_fecha_horario(
        self,
        id_fisioterapeuta,
        fecha,
        id_horario
    ):

        return (
            self.db.query(Cita)
            .filter(
                Cita.id_fisioterapeuta ==
                id_fisioterapeuta,
                Cita.fecha == fecha,
                Cita.id_horario ==
                id_horario,
                Cita.estado ==
                "programada"
            )
            .first()
        )

    # ==========================================================
    # CREAR
    # ==========================================================

    def create(self, cita):

        nueva = Cita(

            fecha=cita.fecha,

            motivo=cita.motivo,

            estado=cita.estado,

            id_paciente=cita.id_paciente,

            id_horario=cita.id_horario,

            id_fisioterapeuta=
                cita.id_fisioterapeuta
        )

        self.db.add(nueva)

        self.db.commit()

        self.db.refresh(nueva)

        return nueva

    # ==========================================================
    # ACTUALIZAR
    # ==========================================================

    def update(self, id, cita):

        existente = self.get_by_id(id)

        if not existente:
            return None

        if isinstance(cita, dict):

            if "fecha" in cita:
                existente.fecha = cita["fecha"]

            if "motivo" in cita:
                existente.motivo = cita["motivo"]

            if "id_horario" in cita:
                existente.id_horario = cita["id_horario"]

            if "estado" in cita:
                existente.estado = cita["estado"]

        else:

            existente.fecha = cita.fecha

            existente.motivo = cita.motivo

            existente.id_horario = cita.id_horario

        self.db.commit()

        self.db.refresh(existente)

        return existente