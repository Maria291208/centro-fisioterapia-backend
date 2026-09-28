from datetime import date
from fastapi import HTTPException

from app.domain.entities.reporte import Reporte


class GenerarReporte:

    def __init__(
        self,
        reporte_repo,
        tratamiento_repo,
        sesion_repo,
        asistencia_repo
    ):
        self.reporte_repo = reporte_repo
        self.tratamiento_repo = tratamiento_repo
        self.sesion_repo = sesion_repo
        self.asistencia_repo = asistencia_repo

    def ejecutar(self, datos):

        tratamiento = self.tratamiento_repo.get_by_id(
            datos.id_tratamiento
        )

        if not tratamiento:
            raise HTTPException(
                status_code=404,
                detail="El tratamiento no existe"
            )

        sesiones = self.sesion_repo.get_by_tratamiento(
            datos.id_tratamiento
        )

        if not sesiones:
            porcentaje = 0
        else:
            asistencias = 0

            for sesion in sesiones:
                asistencia = self.asistencia_repo.get_by_sesion(
                    sesion.id
                )

                if asistencia and asistencia.estado == "presente":
                    asistencias += 1

            porcentaje = (asistencias / len(sesiones)) * 100

        reporte = Reporte(
            fecha_generacion=date.today(),
            periodo=datos.periodo,
            porcentaje_cumplimiento=porcentaje,
            id_tratamiento=datos.id_tratamiento
        )

        return self.reporte_repo.create(reporte)