from fastapi import APIRouter
from controllers.solicitud_controller import solicitud_controller

solicitud_router = APIRouter()
solicitud_router.include_router(solicitud_controller, prefix="/solicitudes", tags=["solicitudes"])
