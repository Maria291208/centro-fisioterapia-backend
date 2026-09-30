from fastapi import HTTPException

from app.infrastructure.database.repositories.cita_repository import CitaRepository


class ModificarCita:

    def __init__(
        self,
        cita_repo,
        sesion_repo
    ):
        self.cita_repo = cita_repo
        self.sesion_repo = sesion_repo

    def ejecutar(
        self,
        cita_id: int,
        datos
    ):

        cita = self.cita_repo.get_by_id(cita_id)

        if not cita:
            raise HTTPException(
                status_code=404,
                detail="Cita no encontrada"
            )

        datos_dict = datos.model_dump(
            exclude_unset=True
        )

        nueva_fecha = datos_dict.get(
            "fecha",
            cita.fecha
        )

        nuevo_horario = datos_dict.get(
            "id_horario",
            cita.id_horario
        )
        cita_paciente = (
            self.cita_repo
            .get_by_paciente_fecha_horario(
                cita.id_paciente,
                nueva_fecha,
                nuevo_horario
            )
        )

        if cita_paciente and cita_paciente.id != cita_id:
            raise HTTPException(
                status_code=400,
                detail="El paciente ya tiene otra cita en esa fecha y horario"
            )
        cita_fisioterapeuta = (
            self.cita_repo
            .get_by_fisioterapeuta_fecha_horario(
                cita.id_fisioterapeuta,
                nueva_fecha,
                nuevo_horario
            )
        )

        if (
            cita_fisioterapeuta
            and cita_fisioterapeuta.id != cita_id
        ):
            raise HTTPException(
                status_code=400,
                detail="El fisioterapeuta ya tiene otra cita en esa fecha y horario"
            )

        sesion_fisioterapeuta = (
            self.sesion_repo
            .get_by_fisioterapeuta_fecha_horario(
                cita.id_fisioterapeuta,
                nueva_fecha,
                nuevo_horario
            )
        )

        if sesion_fisioterapeuta:
            raise HTTPException(
                status_code=400,
                detail="El fisioterapeuta ya tiene una sesión en esa fecha y horario"
            )

        sesion_paciente = (
            self.sesion_repo
            .get_by_paciente_fecha_horario(
                cita.id_paciente,
                nueva_fecha,
                nuevo_horario
            )
        )

        if sesion_paciente:
            raise HTTPException(
                status_code=400,
                detail="El paciente ya tiene una sesión en esa fecha y horario"
            )

        return self.cita_repo.update(
            cita_id,
            datos_dict
        )