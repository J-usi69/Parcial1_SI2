from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class RecomendacionSucursalBase(BaseModel):
    solicitud_id: int
    sucursal_recomendada_id: int
    score_recomendacion: float
    criterios_evaluados: dict
    justificacion_recomendacion: str
    precio_estimado: Optional[float] = None
    distancia_estimada: Optional[float] = None

class RecomendacionSucursalCreate(RecomendacionSucursalBase):
    pass

class RecomendacionSucursalResponse(RecomendacionSucursalBase):
    id: int
    recomendacion_activa: bool
    creada_por_ia: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
