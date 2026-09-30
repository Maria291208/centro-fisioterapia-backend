from fastapi import HTTPException

from app.domain.entities.sesion import Sesion


class ProgramarSesion:

    def __init__(
        self,
        sesion_repo,
        tratamiento_repo,
        horario_repo
    ):

        self.sesion_repo = sesion_repo

        self.tratamiento_repo = tratamiento_repo

        self.horario_repo = horario_repo

    def ejecutar(self, datos):

        tratamiento = self.tratamiento_repo.get_by_id(
            datos.id_tratamiento
        )

        if not tratamiento:

            raise HTTPException(
                status_code=404,
                detail="El tratamiento no existe"
            )

        if datos.numero_sesion > tratamiento.numero_sesiones:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"El tratamiento tiene establecidas "
                    f"{tratamiento.numero_sesiones} sesiones. "
                    f"No puede registrar la sesión "
                    f"{datos.numero_sesion}."
                )
            )

   
        sesiones_existentes = (
            self.sesion_repo.get_by_tratamiento(
                datos.id_tratamiento
            )
        )

        if len(sesiones_existentes) >= tratamiento.numero_sesiones:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Ya se alcanzó el número máximo de "
                    "sesiones establecido para este tratamiento"
                )
            )

    
        if datos.fecha < tratamiento.fecha_inicio:

            raise HTTPException(
                status_code=400,
                detail=(
                    "La fecha de la sesión no puede ser "
                    "anterior al inicio del tratamiento"
                )
            )

        if datos.fecha > tratamiento.fecha_fin:

            raise HTTPException(
                status_code=400,
                detail=(
                    "La fecha de la sesión no puede superar "
                    "la fecha de fin del tratamiento"
                )
            )

  
        sesion_fecha = (
            self.sesion_repo
            .get_by_tratamiento_fecha(
                datos.id_tratamiento,
                datos.fecha
            )
        )

        if sesion_fecha:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Ya existe una sesión de este tratamiento "
                    "en esa fecha"
                )
            )

        sesion_numero = (
            self.sesion_repo
            .get_by_tratamiento_numero(
                datos.id_tratamiento,
                datos.numero_sesion
            )
        )

        if sesion_numero:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El número de sesión ya existe "
                    "en este tratamiento"
                )
            )

        horario = self.horario_repo.get_by_id(
            datos.id_horario
        )

        if not horario:

            raise HTTPException(
                status_code=404,
                detail="El horario no existe"
            )


        sesion = Sesion(

            fecha=datos.fecha,

            numero_sesion=datos.numero_sesion,

            id_tratamiento=datos.id_tratamiento,

            id_horario=datos.id_horario
        )

        return self.sesion_repo.create(
            sesion
        )