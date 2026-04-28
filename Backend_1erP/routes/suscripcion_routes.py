from fastapi import APIRouter
from controllers.suscripcion_controller import suscripcion_controller

suscripcion_router = APIRouter()
suscripcion_router.include_router(suscripcion_controller, prefix="/suscripciones", tags=["suscripciones"])
