class Sesion:

    def __init__(
        self,
        id=None,
        fecha=None,
        numero_sesion=None,
        estado="prescrita",
        motivo_reprogramacion=None,
        id_tratamiento=None,
        id_horario=None
    ):

        self.id = id

        self.fecha = fecha

        self.numero_sesion = numero_sesion

        self.estado = estado

        self.motivo_reprogramacion = motivo_reprogramacion

        self.id_tratamiento = id_tratamiento

        self.id_horario = id_horario