class Evaluacion:
    def __init__(
        self,
        id: int,
        fecha,
        diagnostico: str,
        id_cita: int
    ):
        self.id = id
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.id_cita = id_cita