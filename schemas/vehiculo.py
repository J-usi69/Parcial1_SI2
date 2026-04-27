from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.enums import MarcaVehiculo

class VehiculoBase(BaseModel):
    usuario_id: int
    marca: MarcaVehiculo
    modelo: str
    placa: str
    anio: int
    color: Optional[str] = None
    cilindrada: Optional[str] = None
    foto: Optional[str] = None
    status: str = "activo"

class VehiculoCreate(VehiculoBase):
    pass

class VehiculoUpdate(BaseModel):
    marca: Optional[MarcaVehiculo] = None
    modelo: Optional[str] = None
    placa: Optional[str] = None
    anio: Optional[int] = None
    color: Optional[str] = None
    cilindrada: Optional[str] = None
    foto: Optional[str] = None
    status: Optional[str] = None

class VehiculoResponse(VehiculoBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
