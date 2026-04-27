from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from db import Base

class Archivo(Base):
    __tablename__ = "archivos"

    id = Column(Integer, primary_key=True, index=True)
    entidad_tipo = Column(String, nullable=False, index=True) # "solicitud", "diagnostico", "pago"
    entidad_id = Column(Integer, nullable=False, index=True)
    
    nombre_original = Column(String, nullable=False)
    nombre_interno = Column(String, nullable=False, unique=True)
    mime_type = Column(String, nullable=False)
    tamano_bytes = Column(Integer, nullable=True)
    ruta = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    status = Column(String, default="activo", nullable=False)
    
    subido_por_id = Column(Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
