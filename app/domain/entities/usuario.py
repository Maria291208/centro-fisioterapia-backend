class Usuario:

    def __init__(
        self,
        id=None,
        username=None,
        password_hash=None,
        rol="paciente",
        active=True,
        id_paciente=None
    ):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.rol = rol
        self.active = active
        self.id_paciente = id_paciente