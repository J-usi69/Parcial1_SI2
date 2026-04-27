from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime
from sqlalchemy.sql import func
from db import Base

class Suscripcion(Base):
    __tablename__ = "suscripciones"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False) # Precision y Escala monetaria real
    duracion = Column(Integer, nullable=False) # Representado en dias
    max_sucursales = Column(Integer, default=1, nullable=False)
    max_usuarios = Column(Integer, default=1, nullable=False)
    estado = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())