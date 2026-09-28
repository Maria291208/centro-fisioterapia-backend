from fastapi import HTTPException

from app.infrastructure.database.repositories.evaluacion_repository import EvaluacionRepository
from app.infrastructure.database.repositories.cita_repository import CitaRepository

from app.presentation.api.schemas.evaluacion import EvaluacionCreate


class RegistrarEvaluacion:

    def __init__(
        self,
        evaluacion_repository: EvaluacionRepository,
        cita_repository: CitaRepository
    ):
        self.evaluacion_repository = evaluacion_repository
        self.cita_repository = cita_repository

    def ejecutar(self, datos: EvaluacionCreate, usuario):

        cita = self.cita_repository.get_by_id(datos.id_cita)

        if not cita:
            raise HTTPException(
                status_code=404,
                detail="Cita no encontrada"
            )

        # El fisioterapeuta debe ser el mismo asignado a la cita
        if usuario.rol == "fisioterapeuta":
            if cita.id_fisioterapeuta != usuario.id:
                raise HTTPException(
                    status_code=403,
                    detail="Solo puede evaluar citas asignadas a usted"
                )

        # La evaluación debe realizarse el mismo día de la cita
        if datos.fecha != cita.fecha:
            raise HTTPException(
                status_code=400,
                detail="La fecha de la evaluación debe ser la misma fecha de la cita"
            )

        evaluacion_existente = (
            self.evaluacion_repository
            .get_by_cita(datos.id_cita)
        )

        if evaluacion_existente:
            raise HTTPException(
                status_code=400,
                detail="La cita ya tiene una evaluación"
            )

        evaluacion_data = datos.model_dump()

        evaluacion = self.evaluacion_repository.create(
            evaluacion_data
        )

        # Al realizarse la evaluación, la cita pasa a atendida
        self.cita_repository.update(
            datos.id_cita,
            {
                "estado": "atendida"
            }
        )

        return evaluacion