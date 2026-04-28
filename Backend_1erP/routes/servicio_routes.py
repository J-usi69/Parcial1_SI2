from fastapi import APIRouter
from controllers.servicio_controller import servicio_controller

servicio_router = APIRouter()
servicio_router.include_router(servicio_controller, prefix="/servicios", tags=["servicios"])
