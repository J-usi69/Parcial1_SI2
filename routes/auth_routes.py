from fastapi import APIRouter
from controllers.auth_controller import auth_controller

auth_router = APIRouter()
auth_router.include_router(auth_controller, prefix="/auth", tags=["auth"])
