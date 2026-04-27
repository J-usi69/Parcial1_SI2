from pydantic import BaseModel, EmailStr, field_validator
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
    sucursal_id: Optional[int] = None
    suscripcion_id: int

class UsuarioCreate(UsuarioBase):
    password: str # Regla Pydantic expuesta solo a la creación

    @field_validator('fecha_nac')
    @classmethod
    def validar_mayoria_edad(cls, v):
        if v:
            today = date.today()
            edad = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
            if edad < 18:
                raise ValueError("El usuario debe ser mayor de edad (18 años o más).")
        return v
        
class RegistroClienteRequest(BaseModel):
    ci: Optional[str] = None
    nombres: str
    apellidos: str
    correo: EmailStr
    telefono: Optional[str] = None
    fecha_nac: Optional[date] = None
    foto_perfil: Optional[str] = None
    password: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "ci": "1234567",
                "nombres": "Juan",
                "apellidos": "Perez",
                "correo": "juan@cliente.com",
                "telefono": "70000000",
                "fecha_nac": "1990-01-01",
                "password": "password123"
            }
        }
    }
    
    @field_validator('fecha_nac')
    @classmethod
    def validar_mayoria_edad(cls, v):
        if v:
            today = date.today()
            edad = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
            if edad < 18:
                raise ValueError("El usuario debe ser mayor de edad (18 años o más).")
        return v

class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    foto_perfil: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    is_active: bool
    is_staff: bool
    is_owner: bool
    last_con: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "nombres": "Juan",
                "apellidos": "Perez",
                "correo": "juan@veltra.com",
                "type": "Cliente",
                "is_active": True,
                "is_staff": False,
                "is_owner": False,
                "empresa_id": None,
                "sucursal_id": None,
                "suscripcion_id": 1
            }
        }
    }
