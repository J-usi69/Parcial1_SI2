from fastapi import APIRouter
from controllers.servicio_sucursal_controller import servicio_sucursal_controller

servicio_sucursal_router = APIRouter()
servicio_sucursal_router.include_router(servicio_sucursal_controller, prefix="/servicios-sucursales", tags=["servicios-sucursales"])
