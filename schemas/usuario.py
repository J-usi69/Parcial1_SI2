from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from models.enums import TipoUsuario

class UsuarioBase(BaseModel):
    ci: Optional[str] = None
    nombres: str
    apellidos: str
    correo: EmailStr # Validacion propia sintactica
    telefono: Optional[str] = None
    fecha_nac: Optional[date] = None
    type: TipoUsuario
    foto_perfil: Optional[str] = None
    empresa_id: Optional[int] = None
    suscripcion_id: int

class UsuarioCreate(UsuarioBase):
    password: str # Regla Pydantic expuesta solo a la creación

class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    foto_perfil: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    is_active: bool
    is_staff: bool
    last_con: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
