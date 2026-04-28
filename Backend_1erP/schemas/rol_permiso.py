from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RolPermisoBase(BaseModel):
    rol_id: int
    permiso_id: int
    vigente: bool = True

class RolPermisoCreate(RolPermisoBase):
    pass

class RolPermisoUpdate(BaseModel):
    vigente: bool # Solo se expone la mutacion de vigencia

class RolPermisoResponse(RolPermisoBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
