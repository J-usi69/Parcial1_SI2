from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.enums import EstadoOrganizacion

class EmpresaBase(BaseModel):
    nit: str
    razon_soc: str
    nombre: str
    status: EstadoOrganizacion = EstadoOrganizacion.activo

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(BaseModel):
    nit: Optional[str] = None
    razon_soc: Optional[str] = None
    nombre: Optional[str] = None
    status: Optional[EstadoOrganizacion] = None

class EmpresaResponse(EmpresaBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
