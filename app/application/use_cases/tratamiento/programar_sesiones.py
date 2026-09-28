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

        # ==========================================
        # 1. Verificar tratamiento
        # ==========================================

        tratamiento = self.tratamiento_repo.get_by_id(
            datos.id_tratamiento
        )

        if not tratamiento:
            raise HTTPException(
                status_code=404,
                detail="El tratamiento no existe"
            )

        # ==========================================
        # 2. Validar fecha del tratamiento
        # ==========================================

        if datos.fecha < tratamiento.fecha_inicio:

            raise HTTPException(
                status_code=400,
                detail="La fecha de la sesión no puede ser anterior al inicio del tratamiento"
            )

        if datos.fecha > tratamiento.fecha_fin:

            raise HTTPException(
                status_code=400,
                detail="La fecha de la sesión no puede superar la fecha de fin del tratamiento"
            )

        # ==========================================
        # 3. Verificar que no exista otra sesión
        #    del mismo tratamiento en esa fecha
        # ==========================================

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
                detail="Ya existe una sesión de este tratamiento en esa fecha"
            )

        # ==========================================
        # 4. Verificar que no se repita
        #    el número de sesión
        # ==========================================

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
                detail="El número de sesión ya existe en este tratamiento"
            )

        # ==========================================
        # 5. Verificar horario
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
        # 6. Crear sesión
        # ==========================================

        sesion = Sesion(
            fecha=datos.fecha,
            numero_sesion=datos.numero_sesion,
            id_tratamiento=datos.id_tratamiento,
            id_horario=datos.id_horario
        )

        # IMPORTANTE:
        # Ya NO cambiamos el horario a "ocupado".
        #
        # Los horarios representan franjas horarias
        # que pueden reutilizarse.

        return self.sesion_repo.create(sesion)