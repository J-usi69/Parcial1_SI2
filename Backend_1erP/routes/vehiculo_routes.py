from fastapi import APIRouter
from controllers.vehiculo_controller import vehiculo_controller

vehiculo_router = APIRouter()
vehiculo_router.include_router(vehiculo_controller, prefix="/vehiculos", tags=["vehiculos"])
