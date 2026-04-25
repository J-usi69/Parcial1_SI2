from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.enums import EstadoOrganizacion

class SucursalBase(BaseModel):
    empresa_id: int
    nombre: str
    direccion: str
    coordenadas: Optional[str] = None
    telefono: Optional[str] = None
    status: EstadoOrganizacion = EstadoOrganizacion.activo

class SucursalCreate(SucursalBase):
    pass

class SucursalUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    coordenadas: Optional[str] = None
    telefono: Optional[str] = None
    status: Optional[EstadoOrganizacion] = None

class SucursalResponse(SucursalBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
