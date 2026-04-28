from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import Base

class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id", ondelete="RESTRICT"), nullable=False)
    servicio_sucursal_id = Column(Integer, ForeignKey("servicios_sucursales.id", ondelete="RESTRICT"), nullable=False)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id", ondelete="CASCADE"), nullable=False)
    
    estado = Column(String, default="pendiente_taller", nullable=False)
    descripcion = Column(String, nullable=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    
    fecha_reporte = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_cierre = Column(DateTime(timezone=True), nullable=True)
    
    motivo_rechazo = Column(String, nullable=True)
    motivo_cancelacion = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
