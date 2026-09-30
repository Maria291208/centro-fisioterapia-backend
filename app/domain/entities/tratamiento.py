class Tratamiento:

    def __init__(
        self,
        id=None,
        fecha_inicio=None,
        fecha_fin=None,
        objetivo=None,
        numero_sesiones=None,
        estado="activo",
        id_evaluacion=None
    ):
        self.id = id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.objetivo = objetivo
        self.numero_sesiones = numero_sesiones
        self.estado = estado
        self.id_evaluacion = id_evaluacion