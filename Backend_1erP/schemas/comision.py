from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ComisionBase(BaseModel):
    solicitud_id: int
    tecnico_id: int
    pago_id: int
    monto_base: float
    porcentaje_comision: float = 10.0
    observacion: Optional[str] = None

class ComisionCreate(ComisionBase):
    pass

class ComisionUpdate(BaseModel):
    pagado: Optional[bool] = None
    observacion: Optional[str] = None

class ComisionResponse(ComisionBase):
    id: int
    monto_comision: float
    pagado: bool
    fecha_calculo: datetime
    fecha_pago_comision: Optional[datetime] = None
    registrado_por_usuario_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
