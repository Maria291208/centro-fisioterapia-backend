from fastapi import HTTPException

from app.domain.entities.tratamiento import Tratamiento


class RegistrarTratamiento:

    def __init__(
        self,
        tratamiento_repo,
        evaluacion_repo
    ):
        self.tratamiento_repo = tratamiento_repo
        self.evaluacion_repo = evaluacion_repo

    def ejecutar(self, datos):

        # Verificar que la evaluación exista
        evaluacion = self.evaluacion_repo.get_by_id(
            datos.id_evaluacion
        )

        if not evaluacion:
            raise HTTPException(
                status_code=404,
                detail="La evaluación no existe"
            )

        # El tratamiento no puede comenzar antes
        # de la evaluación inicial
        if datos.fecha_inicio < evaluacion.fecha:

            raise HTTPException(
                status_code=400,
                detail="La fecha de inicio del tratamiento no puede ser anterior a la evaluación inicial"
            )

        # La fecha de fin debe ser posterior
        # a la fecha de inicio
        if datos.fecha_fin <= datos.fecha_inicio:

            raise HTTPException(
                status_code=400,
                detail="La fecha de fin debe ser posterior a la fecha de inicio"
            )

        # Debe existir al menos una sesión
        if datos.numero_sesiones <= 0:

            raise HTTPException(
                status_code=400,
                detail="El número de sesiones debe ser mayor a cero"
            )

        # No permitir dos tratamientos
        # para la misma evaluación
        existente = self.tratamiento_repo.get_by_evaluacion(
            datos.id_evaluacion
        )

        if existente:

            raise HTTPException(
                status_code=400,
                detail="La evaluación ya tiene un tratamiento"
            )

        tratamiento = Tratamiento(

            fecha_inicio=datos.fecha_inicio,

            fecha_fin=datos.fecha_fin,

            objetivo=datos.objetivo,

            numero_sesiones=datos.numero_sesiones,

            id_evaluacion=datos.id_evaluacion
        )

        return self.tratamiento_repo.create(
            tratamiento
        )