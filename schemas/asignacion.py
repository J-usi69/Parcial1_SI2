from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.enums import EstadoAsignacion

class AsignacionBase(BaseModel):
    solicitud_id: int
    tecnico_id: int

class AsignacionCreate(AsignacionBase):
    pass

class AsignacionResponder(BaseModel):
    """Usado por el Técnico para aceptar o rechazar una asignación."""
    estado: EstadoAsignacion  # solo: aceptada | rechazada

class AsignacionResponse(AsignacionBase):
    id: int
    estado: EstadoAsignacion
    fecha_asignacion: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
