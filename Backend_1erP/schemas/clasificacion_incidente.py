from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from models.enums import EstadoRevisionClasificacion

class ClasificacionIncidenteBase(BaseModel):
    solicitud_id: int
    categoria_incidente: str
    subcategoria_incidente: Optional[str] = None
    nivel_prioridad: str
    requiere_grua: bool = False
    requiere_tecnico_especializado: bool = False
    observaciones_modelo: Optional[str] = None
    confianza_modelo: Optional[float] = None
    fuente_clasificacion: str

class ClasificacionIncidenteCreate(ClasificacionIncidenteBase):
    pass

class ClasificacionIncidenteReport(BaseModel):
    motivo_reporte_cliente: str

class ClasificacionIncidenteRevalidate(BaseModel):
    estado_revision: EstadoRevisionClasificacion
    observacion_revision: Optional[str] = None

class ClasificacionIncidenteResponse(ClasificacionIncidenteBase):
    id: int
    estado_revision: EstadoRevisionClasificacion
    reportada_como_incorrecta: bool
    motivo_reporte_cliente: Optional[str] = None
    revisada_por_usuario_id: Optional[int] = None
    observacion_revision: Optional[str] = None
    fecha_revision: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
