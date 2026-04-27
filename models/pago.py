from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import Base

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id", ondelete="CASCADE"), nullable=False, unique=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False)
    
    metodo_pago_tipo = Column(String, nullable=False)
    metodo_pago_referencia_id = Column(Integer, ForeignKey("metodos_pago.id", ondelete="SET NULL"), nullable=True)
    
    proveedor_pasarela = Column(String, nullable=True)
    referencia_externa = Column(String, nullable=True) # Stripe payment_intent_id
    
    monto = Column(Float, nullable=False)
    estado_pago = Column(String, default="pendiente", nullable=False)
    fecha_pago = Column(DateTime(timezone=True), nullable=True)
    
    verificado_por_usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    fecha_verificacion = Column(DateTime(timezone=True), nullable=True)
    observacion = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
