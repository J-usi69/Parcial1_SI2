from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServicioSucursalBase(BaseModel):
    servicio_id: int
    sucursal_id: int
    precio_local: float
    disponible: bool = True

class ServicioSucursalCreate(ServicioSucursalBase):
    pass

class ServicioSucursalUpdate(BaseModel):
    precio_local: Optional[float] = None
    disponible: Optional[bool] = None

class ServicioSucursalResponse(ServicioSucursalBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
