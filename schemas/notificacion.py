from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.enums import EstadoNotificacion, DestinatarioNotificacion

class NotificacionBase(BaseModel):
    usuario_id: int
    titulo: str
    descripcion: str
    ruta_destino: Optional[str] = None
    status: EstadoNotificacion = EstadoNotificacion.pendiente
    user_type: DestinatarioNotificacion

class NotificacionCreate(NotificacionBase):
    # Omitimos fecha_envio para obligar al backend a forjarla
    pass

class NotificacionResponse(NotificacionBase):
    id: int
    fecha_envio: datetime # Recién exhalada como salida
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
