class Paciente:

    def __init__(
        self,
        id=None,
        nombre=None,
        apellido=None,
        ci=None,
        telefono=None,
        direccion=None,
        fecha_nacimiento=None
    ):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.ci = ci
        self.telefono = telefono
        self.direccion = direccion
        self.fecha_nacimiento = fecha_nacimiento