from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from db import Base

class ClasificacionIncidente(Base):
    __tablename__ = "clasificaciones_incidente"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id", ondelete="CASCADE"), nullable=False)
    
    categoria_incidente = Column(String, nullable=False)
    subcategoria_incidente = Column(String, nullable=True)
    nivel_prioridad = Column(String, nullable=False)
    requiere_grua = Column(Boolean, default=False)
    requiere_tecnico_especializado = Column(Boolean, default=False)
    
    observaciones_modelo = Column(String, nullable=True)
    confianza_modelo = Column(Float, nullable=True)
    fuente_clasificacion = Column(String, nullable=False)
    
    estado_revision = Column(String, default="pendiente", nullable=False)
    reportada_como_incorrecta = Column(Boolean, default=False)
    motivo_reporte_cliente = Column(String, nullable=True)
    
    revisada_por_usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    observacion_revision = Column(String, nullable=True)
    fecha_revision = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
