from fastapi import HTTPException

from app.domain.entities.cita import Cita


class RegistrarCita:

    def __init__(
        self,
        cita_repo,
        horario_repo,
        paciente_repo,
        usuario_repo,
        sesion_repo
    ):
        self.cita_repo = cita_repo
        self.horario_repo = horario_repo
        self.paciente_repo = paciente_repo
        self.usuario_repo = usuario_repo
        self.sesion_repo = sesion_repo

    def ejecutar(self, datos):

        # ==========================================
        # 1. Verificar paciente
        # ==========================================

        paciente = self.paciente_repo.get_by_id(
            datos.id_paciente
        )

        if not paciente:
            raise HTTPException(
                status_code=404,
                detail="El paciente no existe"
            )

        # ==========================================
        # 2. Verificar horario
        # ==========================================

        horario = self.horario_repo.get_by_id(
            datos.id_horario
        )

        if not horario:
            raise HTTPException(
                status_code=404,
                detail="El horario no existe"
            )

        # ==========================================
        # 3. Verificar fisioterapeuta
        # ==========================================

        fisioterapeuta = self.usuario_repo.get_by_id(
            datos.id_fisioterapeuta
        )

        if not fisioterapeuta:
            raise HTTPException(
                status_code=404,
                detail="El fisioterapeuta no existe"
            )

        if fisioterapeuta.rol != "fisioterapeuta":
            raise HTTPException(
                status_code=400,
                detail="El usuario seleccionado no es fisioterapeuta"
            )

        # ==========================================
        # 4. Paciente ya tiene otra CITA
        # ==========================================

        cita_paciente = (
            self.cita_repo
            .get_by_paciente_fecha_horario(
                datos.id_paciente,
                datos.fecha,
                datos.id_horario
            )
        )

        if cita_paciente:
            raise HTTPException(
                status_code=400,
                detail="El paciente ya tiene una cita en esa fecha y horario"
            )

        # ==========================================
        # 5. Fisioterapeuta ya tiene otra CITA
        # ==========================================

        cita_fisioterapeuta = (
            self.cita_repo
            .get_by_fisioterapeuta_fecha_horario(
                datos.id_fisioterapeuta,
                datos.fecha,
                datos.id_horario
            )
        )

        if cita_fisioterapeuta:
            raise HTTPException(
                status_code=400,
                detail="El fisioterapeuta ya tiene una cita en esa fecha y horario"
            )

        # ==========================================
        # 6. Fisioterapeuta ya tiene una SESIÓN
        # ==========================================

        sesion_fisioterapeuta = (
            self.sesion_repo
            .get_by_fisioterapeuta_fecha_horario(
                datos.id_fisioterapeuta,
                datos.fecha,
                datos.id_horario
            )
        )

        if sesion_fisioterapeuta:
            raise HTTPException(
                status_code=400,
                detail="El fisioterapeuta ya tiene una sesión en esa fecha y horario"
            )

        # ==========================================
        # 7. Paciente ya tiene una SESIÓN
        # ==========================================

        sesion_paciente = (
            self.sesion_repo
            .get_by_paciente_fecha_horario(
                datos.id_paciente,
                datos.fecha,
                datos.id_horario
            )
        )

        if sesion_paciente:
            raise HTTPException(
                status_code=400,
                detail="El paciente ya tiene una sesión en esa fecha y horario"
            )

        # ==========================================
        # 8. Crear cita
        # ==========================================

        cita = Cita(
            fecha=datos.fecha,
            motivo=datos.motivo,
            estado="programada",
            id_paciente=datos.id_paciente,
            id_horario=datos.id_horario,
            id_fisioterapeuta=datos.id_fisioterapeuta
        )

        # NO marcar horario como ocupado.
        # El horario puede ser utilizado por
        # diferentes fisioterapeutas.

        return self.cita_repo.create(cita)