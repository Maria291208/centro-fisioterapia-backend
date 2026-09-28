class Horario:
    def __init__(
        self,
        id: int,
        hora_inicio,
        hora_fin,
        estado: str = "disponible"
    ):
        self.id = id
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado