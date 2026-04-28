from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import Base

class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    
    # Dictaminado exclusivamente por Backend
    fecha_envio = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    # Definición Oficial: Ruta de navegación o destino al abrir la notificación
    ruta_destino = Column(String, nullable=True)
    
    status = Column(String, nullable=False) # Enum EstadoNotificacion
    user_type = Column(String, nullable=False) # Enum DestinatarioNotificacion (Audiencia Teorica)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
