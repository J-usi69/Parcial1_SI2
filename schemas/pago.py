from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from models.enums import EstadoPago, TipoMetodoPago

class PagoBase(BaseModel):
    solicitud_id: int
    metodo_pago_tipo: TipoMetodoPago
    metodo_pago_referencia_id: Optional[int] = None
    proveedor_pasarela: Optional[str] = None
    referencia_externa: Optional[str] = None
    monto: float
    observacion: Optional[str] = None

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel):
    estado_pago: Optional[EstadoPago] = None
    referencia_externa: Optional[str] = None
    observacion: Optional[str] = None

class PagoVerify(BaseModel):
    observacion: Optional[str] = None

class PagoResponse(PagoBase):
    id: int
    cliente_id: int
    estado_pago: EstadoPago
    fecha_pago: Optional[datetime] = None
    verificado_por_usuario_id: Optional[int] = None
    fecha_verificacion: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
