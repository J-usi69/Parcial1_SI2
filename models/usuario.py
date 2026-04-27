from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
import sqlalchemy as sa
from sqlalchemy.sql import func
from db import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    ci = Column(String, unique=True, nullable=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    telefono = Column(String, nullable=True)
    fecha_nac = Column(Date, nullable=True)
    type = Column(String, nullable=False)
    foto_perfil = Column(String, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_staff = Column(Boolean, default=False, nullable=False)
    is_owner = Column(Boolean, default=False, nullable=False)
    last_con = Column(DateTime, nullable=True)
    
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="SET NULL"), nullable=True)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id", ondelete="SET NULL"), nullable=True)
    suscripcion_id = Column(Integer, ForeignKey("suscripciones.id", ondelete="RESTRICT"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        # Asegurar a nivel de base de datos que solo exista un owner activo por empresa
        sa.Index('ix_unique_owner_per_empresa', 'empresa_id', unique=True, postgresql_where=sa.text("is_owner = true")),
    )