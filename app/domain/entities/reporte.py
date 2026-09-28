class Reporte:
    def __init__(
        self,
        id=None,
        fecha_generacion=None,
        periodo=None,
        porcentaje_cumplimiento=None,
        id_tratamiento=None
    ):
        self.id = id
        self.fecha_generacion = fecha_generacion
        self.periodo = periodo
        self.porcentaje_cumplimiento = porcentaje_cumplimiento
        self.id_tratamiento = id_tratamiento