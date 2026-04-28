from fastapi import APIRouter
from controllers.notificacion_usuario_controller import notificacion_usuario_controller

notificacion_usuario_router = APIRouter()
notificacion_usuario_router.include_router(notificacion_usuario_controller, prefix="/bandeja-notificaciones", tags=["bandeja usuario"])
