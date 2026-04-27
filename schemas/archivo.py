from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ArchivoBase(BaseModel):
    entidad_tipo: str
    entidad_id: int
    nombre_original: str
    mime_type: str
    tamano_bytes: Optional[int] = None
    descripcion: Optional[str] = None

class ArchivoCreate(ArchivoBase):
    pass # La ruta y nombre interno se generan en el service

class ArchivoUpdate(BaseModel):
    descripcion: Optional[str] = None
    status: Optional[str] = None

class ArchivoResponse(ArchivoBase):
    id: int
    nombre_interno: str
    ruta: str
    status: str
    subido_por_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
