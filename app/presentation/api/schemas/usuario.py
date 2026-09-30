from pydantic import BaseModel


# ==========================================================
# REGISTRAR USUARIO
# ==========================================================

class UsuarioCreate(BaseModel):

    username: str

    password: str

    rol: str


# ==========================================================
# RESPUESTA USUARIO
# ==========================================================

class UsuarioResponse(BaseModel):

    id: int

    username: str

    rol: str

    active: bool

    id_paciente: int | None = None

    class Config:

        from_attributes = True


# ==========================================================
# CAMBIAR ESTADO DEL USUARIO
# ==========================================================

class UsuarioEstadoUpdate(BaseModel):

    active: bool


# ==========================================================
# LOGIN
# ==========================================================

class Token(BaseModel):

    access_token: str

    token_type: str