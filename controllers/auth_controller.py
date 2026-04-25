from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime

from schemas.auth import LoginRequest, Token
from services.auth_service import AuthService, auth_service_dep
from repositories.usuario_repository import UsuarioRepository
from db import get_db

auth_controller = APIRouter()
security = HTTPBearer()

def get_user_repo():
    return UsuarioRepository()

@auth_controller.post("/login", response_model=Token)
def login(
    request: LoginRequest, 
    db: Session = Depends(get_db),
    auth_svc: AuthService = Depends(auth_service_dep),
    repo: UsuarioRepository = Depends(get_user_repo)
):
    # Verificación en minúscula transversal
    user = repo.get_by_correo(db, request.email.lower())
    
    if not user:
        raise HTTPException(status_code=401, detail="Datos de credencial inválidos.")
        
    if not user.is_active:
        raise HTTPException(status_code=401, detail="La cuenta está actualmente inhabilitada.")
        
    if not auth_svc.verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Datos de credencial inválidos.")
        
    token = auth_svc.create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@auth_controller.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    auth_svc: AuthService = Depends(auth_service_dep),
    repo: UsuarioRepository = Depends(get_user_repo)
):
    # Extrae el identitario, intercepta la Base y forja el evento en el Last-Con
    payload = auth_svc.decode_access_token(credentials.credentials)
    if payload and payload.get("sub"):
        repo.update_last_con(db, int(payload.get("sub")), datetime.utcnow())
        return {"message": "Sesión Cerrada. Desconexión temporal estampada con éxito."}
        
    raise HTTPException(status_code=401, detail="Token estropeado o nulo.")
