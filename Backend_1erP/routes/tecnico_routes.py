from fastapi import APIRouter
from controllers.tecnico_controller import tecnico_controller

tecnico_router = APIRouter()
tecnico_router.include_router(tecnico_controller, prefix="/tecnicos", tags=["tecnicos"])
