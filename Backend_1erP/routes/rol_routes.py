from fastapi import APIRouter
from controllers.rol_controller import rol_controller

rol_router = APIRouter()
rol_router.include_router(rol_controller, prefix="/roles", tags=["roles"])
