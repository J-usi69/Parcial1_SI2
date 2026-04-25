from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PermisoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class PermisoCreate(PermisoBase):
    pass

class PermisoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class PermisoResponse(PermisoBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
