from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from db import Base

class RolPermiso(Base):
    __tablename__ = "rol_permiso"
    __table_args__ = (UniqueConstraint('rol_id', 'permiso_id', name='uq_rol_permiso'),)

    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permiso_id = Column(Integer, ForeignKey("permisos.id", ondelete="CASCADE"), nullable=False)
    vigente = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
