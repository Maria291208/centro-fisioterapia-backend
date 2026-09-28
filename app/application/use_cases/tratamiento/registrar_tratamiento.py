from fastapi import HTTPException

from app.domain.entities.tratamiento import Tratamiento


class RegistrarTratamiento:

    def __init__(self, tratamiento_repo, evaluacion_repo):
        self.tratamiento_repo = tratamiento_repo
        self.evaluacion_repo = evaluacion_repo

    def ejecutar(self, datos):

        if datos.fecha_fin <= datos.fecha_inicio:
            raise HTTPException(
                status_code=400,
                detail="La fecha de fin debe ser posterior a la fecha de inicio"
            )

        evaluacion = self.evaluacion_repo.get_by_id(
            datos.id_evaluacion
        )

        if not evaluacion:
            raise HTTPException(
                status_code=404,
                detail="La evaluación no existe"
            )

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
            id_evaluacion=datos.id_evaluacion
        )

        return self.tratamiento_repo.create(tratamiento)