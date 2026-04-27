from fastapi import APIRouter
from controllers.asignacion_controller import asignacion_controller

asignacion_router = APIRouter()
asignacion_router.include_router(asignacion_controller, prefix="/asignaciones", tags=["asignaciones"])
