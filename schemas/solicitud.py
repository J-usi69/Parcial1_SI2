from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.enums import EstadoSolicitud

class SolicitudBase(BaseModel):
    cliente_id: int
    vehiculo_id: int
    # FK explícita a servicios_sucursales — no a servicios directamente
    servicio_sucursal_id: int
    sucursal_id: int
    descripcion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class SolicitudCreate(SolicitudBase):
    pass

class SolicitudUpdate(BaseModel):
    estado: Optional[EstadoSolicitud] = None
    motivo_rechazo: Optional[str] = None
    motivo_cancelacion: Optional[str] = None
    fecha_cierre: Optional[datetime] = None

class SolicitudResponse(SolicitudBase):
    id: int
    estado: EstadoSolicitud
    fecha_reporte: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None
    motivo_rechazo: Optional[str] = None
    motivo_cancelacion: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
