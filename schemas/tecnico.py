from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.enums import EstadoTecnico

class TecnicoBase(BaseModel):
    usuario_id: int
    especialidad: Optional[str] = None
    estado_operativo: EstadoTecnico = EstadoTecnico.activo

class TecnicoCreate(TecnicoBase):
    pass

class TecnicoUpdate(BaseModel):
    especialidad: Optional[str] = None
    estado_operativo: Optional[EstadoTecnico] = None

class TecnicoResponse(TecnicoBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
