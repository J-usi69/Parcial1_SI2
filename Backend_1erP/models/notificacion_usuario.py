from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from db import Base

class NotificacionUsuario(Base):
    __tablename__ = "notificacion_usuario"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    notificacion_id = Column(Integer, ForeignKey("notificaciones.id", ondelete="CASCADE"), nullable=False)
    leido = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('usuario_id', 'notificacion_id', name='uq_notif_usuario'),
    )
