from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import Base

class Diagnostico(Base):
    __tablename__ = "diagnosticos"

    id = Column(Integer, primary_key=True, index=True)
    asignacion_id = Column(Integer, ForeignKey("asignaciones.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    descripcion = Column(String, nullable=False)
    costo_estimado = Column(Float, nullable=True)
    estado = Column(String, default="borrador", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
