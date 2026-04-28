from fastapi import APIRouter
from controllers.usuario_controller import usuario_controller

usuario_router = APIRouter()
usuario_router.include_router(usuario_controller, prefix="/usuarios", tags=["usuarios"])
