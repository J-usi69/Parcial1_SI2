from fastapi import APIRouter
from controllers.sucursal_controller import sucursal_controller

sucursal_router = APIRouter()
sucursal_router.include_router(sucursal_controller, prefix="/sucursales", tags=["sucursales"])
