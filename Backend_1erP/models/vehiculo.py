from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from db import Base

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    placa = Column(String, nullable=False, unique=True, index=True)
    anio = Column(Integer, nullable=False)
    color = Column(String, nullable=True)
    cilindrada = Column(String, nullable=True)
    foto = Column(String, nullable=True)
    status = Column(String, default="activo", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
