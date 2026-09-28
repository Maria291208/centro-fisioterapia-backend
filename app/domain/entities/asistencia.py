class Asistencia:
    def __init__(
        self,
        id=None,
        fecha_registro=None,
        estado=None,
        observaciones=None,
        id_sesion=None
    ):
        self.id = id
        self.fecha_registro = fecha_registro
        self.estado = estado
        self.observaciones = observaciones
        self.id_sesion = id_sesion