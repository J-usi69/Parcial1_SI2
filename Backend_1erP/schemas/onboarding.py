from pydantic import BaseModel
from schemas.usuario import RegistroClienteRequest, UsuarioResponse
from schemas.empresa import EmpresaCreate, EmpresaResponse
from schemas.sucursal import SucursalCreate, SucursalResponse
from models.enums import EstadoOrganizacion
from typing import Optional

class OnboardingSucursalCreate(BaseModel):
    nombre: str
    direccion: str
    coordenadas: Optional[str] = None
    telefono: Optional[str] = None
    status: EstadoOrganizacion = EstadoOrganizacion.activo
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "Veltra Norte",
                "direccion": "Av. Banzer Km 5.5",
                "telefono": "77700001",
                "status": "activo"
            }
        }
    }

class OnboardingTallerRequest(BaseModel):
    admin: RegistroClienteRequest
    empresa: EmpresaCreate
    sucursal: OnboardingSucursalCreate

class OnboardingTallerResponse(BaseModel):
    message: str
    admin: UsuarioResponse
    empresa: EmpresaResponse
    sucursal: SucursalResponse
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Onboarding de taller completado con éxito.",
                "admin": {
                    "nombres": "Juan",
                    "apellidos": "Perez",
                    "correo": "juan@taller.com",
                    "type": "Empresa",
                    "id": 1,
                    "is_active": True,
                    "is_owner": True
                },
                "empresa": {
                    "nit": "123456789",
                    "razon_soc": "Taller Perez S.R.L.",
                    "nombre": "Taller Perez",
                    "id": 1
                },
                "sucursal": {
                    "nombre": "Taller Perez Norte",
                    "direccion": "Av. Banzer",
                    "empresa_id": 1,
                    "id": 1
                }
            }
        }
    }
