from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import Base, DATABASE_URL

from models.rol import Rol
from models.permiso import Permiso
from models.rol_permiso import RolPermiso
from models.empresa import Empresa
from models.sucursal import Sucursal
from models.suscripcion import Suscripcion
from models.usuario import Usuario
from models.rol_usuario import RolUsuario
from models.notificacion import Notificacion
from models.notificacion_usuario import NotificacionUsuario
from models.vehiculo import Vehiculo
from models.servicio import Servicio
from models.servicio_sucursal import ServicioSucursal
from models.tecnico import Tecnico
from models.solicitud import Solicitud
from models.asignacion import Asignacion
from models.diagnostico import Diagnostico

# Bloque F
from models.archivo import Archivo
from models.clasificacion_incidente import ClasificacionIncidente
from models.recomendacion_sucursal import RecomendacionSucursal
from models.metodo_pago import MetodoPago
from models.pago import Pago
from models.comision import Comision

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()