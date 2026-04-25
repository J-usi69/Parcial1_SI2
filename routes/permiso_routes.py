from fastapi import APIRouter
from controllers.permiso_controller import permiso_controller

permiso_router = APIRouter()
permiso_router.include_router(permiso_controller, prefix="/permisos", tags=["permisos"])
