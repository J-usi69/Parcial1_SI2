from fastapi import APIRouter
from controllers.rol_permiso_controller import rol_permiso_controller

rol_permiso_router = APIRouter()
rol_permiso_router.include_router(rol_permiso_controller, prefix="/rol-permisos", tags=["rol_permisos"])
