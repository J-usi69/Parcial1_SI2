from fastapi import APIRouter
from controllers.rol_usuario_controller import rol_usuario_controller

rol_usuario_router = APIRouter()
rol_usuario_router.include_router(rol_usuario_controller, prefix="/rol-usuario", tags=["roles de usuario"])
