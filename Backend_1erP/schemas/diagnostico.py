from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.enums import EstadoDiagnostico

class DiagnosticoBase(BaseModel):
    asignacion_id: int
    descripcion: str
    costo_estimado: Optional[float] = None

class DiagnosticoCreate(DiagnosticoBase):
    pass

class DiagnosticoUpdate(BaseModel):
    descripcion: Optional[str] = None
    costo_estimado: Optional[float] = None
    estado: Optional[EstadoDiagnostico] = None

class DiagnosticoResponse(DiagnosticoBase):
    id: int
    estado: EstadoDiagnostico
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
