from fastapi import HTTPException
from app.domain.entities.evolucion import Evolucion


class RegistrarEvolucion:

    def __init__(self, evolucion_repo, sesion_repo):
        self.evolucion_repo = evolucion_repo
        self.sesion_repo = sesion_repo

    def ejecutar(self, datos):

        sesion = self.sesion_repo.get_by_id(datos.id_sesion)

        if not sesion:
            raise HTTPException(
                status_code=404,
                detail="La sesión no existe"
            )

        evolucion_existente = self.evolucion_repo.get_by_sesion(
            datos.id_sesion
        )

        if evolucion_existente:
            raise HTTPException(
                status_code=400,
                detail="La sesión ya tiene una evolución registrada"
            )

        evolucion = Evolucion(
            fecha=datos.fecha,
            descripcion=datos.descripcion,
            observaciones=datos.observaciones,
            id_sesion=datos.id_sesion
        )

        return self.evolucion_repo.create(evolucion)