from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación de Routers Modulares (Bloques A-D)
from routes.auth_routes import auth_router
from routes.rol_routes import rol_router
from routes.permiso_routes import permiso_router
from routes.rol_permiso_routes import rol_permiso_router
from routes.empresa_routes import empresa_router
from routes.sucursal_routes import sucursal_router
from routes.suscripcion_routes import suscripcion_router
from routes.usuario_routes import usuario_router
from routes.rol_usuario_routes import rol_usuario_router
from routes.notificacion_routes import notificacion_router
from routes.notificacion_usuario_routes import notificacion_usuario_router

app = FastAPI(
    title="Veltra API - Atención de Emergencias Vehiculares",
    description="API Gateway principal para gestión estructural, identidades operativas y autorizaciones base.",
    version="1.0.0"
)

# CORS Policy Base
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Healthcheck Mínimo
@app.get("/", tags=["Health"])
def health_status():
    return {"app": "Veltra API", "status": "operativa", "version": "1.0.0"}

# Inyección Segmentada de Routers (Sin duplicar código, anexados al sufijo v1)
# Nota: Cada uno de estos routers ya define sus prefijos locales (ej: /usuarios, /empresas) y tags semánticos.

# Seguridad / Autorizaciones
app.include_router(auth_router, prefix="/api/v1")
app.include_router(rol_router, prefix="/api/v1")
app.include_router(permiso_router, prefix="/api/v1")
app.include_router(rol_permiso_router, prefix="/api/v1")

# Organización Estructural
app.include_router(empresa_router, prefix="/api/v1")
app.include_router(sucursal_router, prefix="/api/v1")

# Identidades y Accesos
app.include_router(suscripcion_router, prefix="/api/v1")
app.include_router(usuario_router, prefix="/api/v1")
app.include_router(rol_usuario_router, prefix="/api/v1")

# Avisos y Bandejas
app.include_router(notificacion_router, prefix="/api/v1")
app.include_router(notificacion_usuario_router, prefix="/api/v1")

# Observación:
# Omitimos db.Base.metadata.create_all(bind=engine) deliberadamente.
# Mantendremos la gobernanza de tablas sufragada estrictamente sobre la línea 
# de versionamiento dictada por Alembic.
