from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServicioBase(BaseModel):
    empresa_id: int
    nombre: str
    descripcion: Optional[str] = None
    precio_base: float
    status: str = "activo"

class ServicioCreate(ServicioBase):
    pass

class ServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[float] = None
    status: Optional[str] = None

class ServicioResponse(ServicioBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
