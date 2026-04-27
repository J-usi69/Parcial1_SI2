from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from db import Base

class ServicioSucursal(Base):
    __tablename__ = "servicios_sucursales"

    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"), nullable=False)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id", ondelete="CASCADE"), nullable=False)
    precio_local = Column(Float, nullable=False)
    disponible = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('servicio_id', 'sucursal_id', name='uix_servicio_sucursal'),
    )
