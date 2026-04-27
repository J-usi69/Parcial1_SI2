from fastapi import APIRouter
from controllers.diagnostico_controller import diagnostico_controller

diagnostico_router = APIRouter()
diagnostico_router.include_router(diagnostico_controller, prefix="/diagnosticos", tags=["diagnosticos"])
