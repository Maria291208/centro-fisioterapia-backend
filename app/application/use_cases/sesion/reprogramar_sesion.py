from fastapi import HTTPException


class ReprogramarSesion:

    def __init__(
        self,
        sesion_repo,
        tratamiento_repo,
        evaluacion_repo,
        cita_repo,
        horario_repo
    ):
        self.sesion_repo = sesion_repo
        self.tratamiento_repo = tratamiento_repo
        self.evaluacion_repo = evaluacion_repo
        self.cita_repo = cita_repo
        self.horario_repo = horario_repo

    def ejecutar(self, sesion_id, datos):

        # ==========================================================
        # 1. BUSCAR SESIÓN
        # ==========================================================

        sesion = self.sesion_repo.get_by_id(sesion_id)

        if not sesion:
            raise HTTPException(
                status_code=404,
                detail="La sesión no existe"
            )

        # Permitimos reprogramar una sesión prescrita o ausente
        if sesion.estado not in ["prescrita", "ausente"]:

            raise HTTPException(
                status_code=400,
                detail="Esta sesión ya fue realizada y no puede reprogramarse"
            )

        # ==========================================================
        # 2. BUSCAR TRATAMIENTO
        # ==========================================================

        tratamiento = self.tratamiento_repo.get_by_id(
            sesion.id_tratamiento
        )

        if not tratamiento:

            raise HTTPException(
                status_code=404,
                detail="El tratamiento no existe"
            )

        # ==========================================================
        # 3. VALIDAR FECHAS DEL TRATAMIENTO
        # ==========================================================

        if datos.fecha < tratamiento.fecha_inicio:

            raise HTTPException(
                status_code=400,
                detail="La fecha no puede ser anterior al inicio del tratamiento"
            )

        if datos.fecha > tratamiento.fecha_fin:

            raise HTTPException(
                status_code=400,
                detail="La fecha no puede ser posterior al fin del tratamiento"
            )

        # ==========================================================
        # 4. BUSCAR SESIÓN ANTERIOR
        # ==========================================================

        sesion_anterior = None

        if sesion.numero_sesion > 1:

            sesion_anterior = (
                self.sesion_repo
                .get_by_tratamiento_numero(
                    sesion.id_tratamiento,
                    sesion.numero_sesion - 1
                )
            )

            if sesion_anterior:

                if datos.fecha <= sesion_anterior.fecha:

                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "La nueva fecha debe ser posterior "
                            "a la sesión anterior"
                        )
                    )

        # ==========================================================
        # 5. BUSCAR SESIÓN SIGUIENTE
        # ==========================================================

        sesion_siguiente = (
            self.sesion_repo
            .get_by_tratamiento_numero(
                sesion.id_tratamiento,
                sesion.numero_sesion + 1
            )
        )

        if sesion_siguiente:

            if datos.fecha >= sesion_siguiente.fecha:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "La nueva fecha debe ser anterior "
                        "a la sesión siguiente"
                    )
                )

        # ==========================================================
        # 6. VALIDAR HORARIO
        # ==========================================================

        horario = self.horario_repo.get_by_id(
            datos.id_horario
        )

        if not horario:

            raise HTTPException(
                status_code=404,
                detail="El horario seleccionado no existe"
            )

        # ==========================================================
        # 7. OBTENER EVALUACIÓN Y CITA
        # ==========================================================

        evaluacion = self.evaluacion_repo.get_by_id(
            tratamiento.id_evaluacion
        )

        if not evaluacion:

            raise HTTPException(
                status_code=404,
                detail="La evaluación no existe"
            )

        cita = self.cita_repo.get_by_id(
            evaluacion.id_cita
        )

        if not cita:

            raise HTTPException(
                status_code=404,
                detail="La cita no existe"
            )

        # ==========================================================
        # 8. VALIDAR CONFLICTO DEL PACIENTE
        # ==========================================================

        conflicto_paciente = (
            self.sesion_repo
            .get_by_paciente_fecha_horario(
                cita.id_paciente,
                datos.fecha,
                datos.id_horario,
                sesion.id
            )
        )

        if conflicto_paciente:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El paciente ya tiene una sesión "
                    "programada en ese horario"
                )
            )

        # ==========================================================
        # 9. VALIDAR CONFLICTO DEL FISIOTERAPEUTA
        # ==========================================================

        conflicto_fisioterapeuta = (
            self.sesion_repo
            .get_by_fisioterapeuta_fecha_horario(
                cita.id_fisioterapeuta,
                datos.fecha,
                datos.id_horario,
                sesion.id
            )
        )

        if conflicto_fisioterapeuta:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El fisioterapeuta ya tiene una sesión "
                    "programada en ese horario"
                )
            )

        # ==========================================================
        # 10. VALIDAR CONFLICTO CON CITAS DEL PACIENTE
        # ==========================================================

        cita_paciente = (
            self.cita_repo
            .get_by_paciente_fecha_horario(
                cita.id_paciente,
                datos.fecha,
                datos.id_horario
            )
        )

        if cita_paciente:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El paciente ya tiene una cita "
                    "en ese horario"
                )
            )

        # ==========================================================
        # 11. VALIDAR CONFLICTO CON CITAS DEL FISIOTERAPEUTA
        # ==========================================================

        cita_fisio = (
            self.cita_repo
            .get_by_fisioterapeuta_fecha_horario(
                cita.id_fisioterapeuta,
                datos.fecha,
                datos.id_horario
            )
        )

        if cita_fisio:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El fisioterapeuta ya tiene una cita "
                    "en ese horario"
                )
            )

        # ==========================================================
        # 12. ACTUALIZAR SESIÓN
        # ==========================================================

        sesion.fecha = datos.fecha
        sesion.id_horario = datos.id_horario
        sesion.motivo_reprogramacion = (
            datos.motivo_reprogramacion
        )

        # Si estaba ausente y se reprograma,
        # vuelve a quedar pendiente
        if sesion.estado == "ausente":
            sesion.estado = "prescrita"

        return self.sesion_repo.update(
            sesion.id,
            sesion
        )