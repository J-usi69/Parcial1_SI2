from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from db import Base

class Tecnico(Base):
    """
    Extensión operativa 1:1 de Usuario para el rol Técnico.

    VALIDACIONES OBLIGATORIAS — aplicadas en TecnicoService.create_tecnico:
      [1] usuario.type == "empresa"    — Solo usuarios de tipo empresa pueden ser técnicos.
      [2] usuario tiene rol "tecnico"  — El usuario_id debe tener el rol tecnico activo en rol_usuario.
      [3] misma empresa/sucursal       — El técnico debe pertenecer a la misma empresa/sucursal
                                         del administrador que lo registra (tenant isolation).
      [4] relación 1:1 estricta        — Un usuario_id solo puede tener UNA fila en tecnicos
                                         (enforced por UniqueConstraint a nivel de base de datos).
    """
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True, index=True)
    # Constraint DB: garantiza relación 1:1, un usuario no puede ser dos técnicos
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)

    especialidad = Column(String, nullable=True)
    estado_operativo = Column(String, default="activo", nullable=False)  # enum: activo, inactivo, ocupado

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        # Relación 1:1 estricta: un usuario_id solo puede aparecer una vez en tecnicos
        UniqueConstraint("usuario_id", name="uix_tecnico_usuario"),
    )
