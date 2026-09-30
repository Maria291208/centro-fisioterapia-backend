from fastapi import HTTPException

from app.domain.entities.asistencia import Asistencia


class RegistrarAsistencia:

    def __init__(
        self,
        asistencia_repo,
        sesion_repo,
        tratamiento_repo
    ):
        self.asistencia_repo = asistencia_repo
        self.sesion_repo = sesion_repo
        self.tratamiento_repo = tratamiento_repo

    def ejecutar(self, datos):

        # 1. Buscar la sesión
        sesion = self.sesion_repo.get_by_id(
            datos.id_sesion
        )

        if not sesion:
            raise HTTPException(
                status_code=404,
                detail="La sesión no existe"
            )

        # 2. Verificar que la sesión esté pendiente
        if sesion.estado != "prescrita":
            raise HTTPException(
                status_code=400,
                detail="Esta sesión ya fue atendida o controlada"
            )

        # 3. Verificar que no exista asistencia
        asistencia_existente = (
            self.asistencia_repo.get_by_sesion(
                datos.id_sesion
            )
        )

        if asistencia_existente:
            raise HTTPException(
                status_code=400,
                detail="La asistencia ya fue registrada"
            )

        # 4. Verificar el orden de las sesiones
        if sesion.numero_sesion > 1:

            sesion_anterior = (
                self.sesion_repo.get_by_tratamiento_numero(
                    sesion.id_tratamiento,
                    sesion.numero_sesion - 1
                )
            )

            if not sesion_anterior:
                raise HTTPException(
                    status_code=400,
                    detail="La sesión anterior todavía no está programada"
                )

            if sesion_anterior.estado != "realizada":
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "No puede atender esta sesión. "
                        "Primero debe completarse la sesión anterior"
                    )
                )

        # 5. Crear asistencia
        asistencia = Asistencia(
            fecha_registro=datos.fecha_registro,
            estado=datos.estado,
            observaciones=datos.observaciones,
            id_sesion=datos.id_sesion
        )

        nueva_asistencia = (
            self.asistencia_repo.create(
                asistencia
            )
        )

        # 6. Actualizar estado de la sesión
        if datos.estado == "presente":

            sesion.estado = "realizada"

        elif datos.estado == "ausente":

            sesion.estado = "ausente"

        self.sesion_repo.update(
            sesion.id,
            sesion
        )

        # 7. Obtener todas las sesiones del tratamiento
        sesiones = (
            self.sesion_repo.get_by_tratamiento(
                sesion.id_tratamiento
            )
        )

        # 8. Verificar si todas están controladas
        todas_controladas = True

        for sesion_actual in sesiones:

            asistencia_sesion = (
                self.asistencia_repo.get_by_sesion(
                    sesion_actual.id
                )
            )

            if not asistencia_sesion:
                todas_controladas = False
                break

        # 9. Finalizar tratamiento
        if todas_controladas:

            tratamiento = (
                self.tratamiento_repo.get_by_id(
                    sesion.id_tratamiento
                )
            )

            if tratamiento:

                tratamiento.estado = "finalizado"

                self.tratamiento_repo.update(
                    tratamiento.id,
                    tratamiento
                )

        return nueva_asistencia