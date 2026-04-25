from fastapi import APIRouter
from controllers.notificacion_controller import notificacion_controller

notificacion_router = APIRouter()
notificacion_router.include_router(notificacion_controller, prefix="/notificaciones", tags=["notificaciones matriz"])
