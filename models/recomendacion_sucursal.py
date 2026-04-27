from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from db import Base

class RecomendacionSucursal(Base):
    __tablename__ = "recomendaciones_sucursal"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id", ondelete="CASCADE"), nullable=False)
    sucursal_recomendada_id = Column(Integer, ForeignKey("sucursales.id", ondelete="CASCADE"), nullable=False)
    
    score_recomendacion = Column(Float, nullable=False)
    criterios_evaluados = Column(JSON, nullable=False) 
    justificacion_recomendacion = Column(String, nullable=False)
    
    precio_estimado = Column(Float, nullable=True)
    distancia_estimada = Column(Float, nullable=True)
    
    recomendacion_activa = Column(Boolean, default=True)
    creada_por_ia = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
