from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from db import Base

class Comision(Base):
    __tablename__ = "comisiones"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id", ondelete="RESTRICT"), nullable=False, unique=True)
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id", ondelete="RESTRICT"), nullable=False)
    pago_id = Column(Integer, ForeignKey("pagos.id", ondelete="RESTRICT"), nullable=False)
    
    monto_base = Column(Float, nullable=False)
    porcentaje_comision = Column(Float, default=10.0, nullable=False)
    monto_comision = Column(Float, nullable=False)
    
    pagado = Column(Boolean, default=False)
    fecha_calculo = Column(DateTime(timezone=True), nullable=False)
    fecha_pago_comision = Column(DateTime(timezone=True), nullable=True)
    
    registrado_por_usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    observacion = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
