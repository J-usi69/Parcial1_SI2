from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RolUsuarioBase(BaseModel):
    rol_id: int
    usuario_id: int

class RolUsuarioCreate(RolUsuarioBase):
    pass

class RolUsuarioResponse(RolUsuarioBase):
    id: int
    fecha_asignacion: datetime
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
