class Cita:
    def __init__(
        self,
        id: int = None,
        fecha=None,
        motivo: str = None,
        estado: str = "programada",
        id_paciente: int = None,
        id_horario: int = None,
        id_fisioterapeuta: int = None
    ):
        self.id = id
        self.fecha = fecha
        self.motivo = motivo
        self.estado = estado
        self.id_paciente = id_paciente
        self.id_horario = id_horario
        self.id_fisioterapeuta = id_fisioterapeuta