from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class RolResponse(RolBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
