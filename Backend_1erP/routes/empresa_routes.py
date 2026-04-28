from fastapi import APIRouter
from controllers.empresa_controller import empresa_controller

empresa_router = APIRouter()
empresa_router.include_router(empresa_controller, prefix="/empresas", tags=["empresas"])
