from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from models.enums import PropietarioMetodoPago, TipoMetodoPago

class MetodoPagoBase(BaseModel):
    propietario_tipo: PropietarioMetodoPago
    propietario_id: int
    tipo_pago: TipoMetodoPago
    alias: Optional[str] = None
    referencia_token: Optional[str] = None
    qr_imagen_ruta: Optional[str] = None
    datos_adicionales: Optional[str] = None

class MetodoPagoCreate(MetodoPagoBase):
    pass

class MetodoPagoUpdate(BaseModel):
    alias: Optional[str] = None
    qr_imagen_ruta: Optional[str] = None
    datos_adicionales: Optional[str] = None
    status: Optional[str] = None

class MetodoPagoResponse(MetodoPagoBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
