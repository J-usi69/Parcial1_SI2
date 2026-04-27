from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.onboarding import OnboardingTallerRequest, OnboardingTallerResponse
from schemas.usuario import RegistroClienteRequest, UsuarioResponse
from services.onboarding_service import OnboardingService
from services.auth_service import AuthService
from db import get_db

onboarding_controller = APIRouter()

def get_onboarding_service():
    return OnboardingService(AuthService())

@onboarding_controller.post("/taller", response_model=OnboardingTallerResponse)
def registrar_taller(data: OnboardingTallerRequest, db: Session = Depends(get_db), svc: OnboardingService = Depends(get_onboarding_service)):
    try:
        return svc.registrar_taller(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@onboarding_controller.post("/cliente", response_model=UsuarioResponse)
def registrar_cliente(data: RegistroClienteRequest, db: Session = Depends(get_db), svc: OnboardingService = Depends(get_onboarding_service)):
    try:
        return svc.registrar_cliente(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
