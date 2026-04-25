from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class SuscripcionBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    precio: Decimal = Field(..., ge=0, description="El precio no puede ser negativo")
    duracion: int = Field(..., gt=0, description="Duración en días, debe ser mayor a 0")
    estado: bool = True

class SuscripcionCreate(SuscripcionBase):
    pass

class SuscripcionUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = Field(None, ge=0)
    duracion: Optional[int] = Field(None, gt=0)
    estado: Optional[bool] = None

class SuscripcionResponse(SuscripcionBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
