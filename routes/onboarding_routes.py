from fastapi import APIRouter
from controllers.onboarding_controller import onboarding_controller

onboarding_router = APIRouter(prefix="/onboarding", tags=["Onboarding"])
onboarding_router.include_router(onboarding_controller)
