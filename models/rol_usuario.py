from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from db import Base

class RolUsuario(Base):
    __tablename__ = "rol_usuario"

    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    
    # Dato duro de Negocio
    fecha_asignacion = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    # Capa de Auditoría Universal
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('rol_id', 'usuario_id', name='uq_rol_usuario'),
    )
