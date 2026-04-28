from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base

class MetodoPago(Base):
    __tablename__ = "metodos_pago"

    id = Column(Integer, primary_key=True, index=True)
    propietario_tipo = Column(String, nullable=False, index=True) # "cliente", "sucursal"
    propietario_id = Column(Integer, nullable=False, index=True)
    
    tipo_pago = Column(String, nullable=False) # "efectivo", "qr", "pasarela_pago"
    alias = Column(String, nullable=True)
    referencia_token = Column(String, nullable=True) # Stripe payment_method_id o similar
    qr_imagen_ruta = Column(String, nullable=True)
    datos_adicionales = Column(String, nullable=True) # JSON para info extra no sensible
    status = Column(String, default="activo", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
