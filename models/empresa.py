from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nit = Column(String, unique=True, nullable=False)
    razon_soc = Column(String, nullable=False)
    nombre = Column(String, index=True, nullable=False)
    status = Column(String, default="activo", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
