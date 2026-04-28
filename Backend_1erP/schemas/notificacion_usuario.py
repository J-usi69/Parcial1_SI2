from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificacionUsuarioBase(BaseModel):
    usuario_id: int
    notificacion_id: int
    leido: bool = False

class NotificacionUsuarioCreate(NotificacionUsuarioBase):
    pass

class NotificacionUsuarioResponse(NotificacionUsuarioBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
