from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.usuario import UsuarioCreate, UsuarioResponse
from services.usuario_service import UsuarioService
from repositories.usuario_repository import UsuarioRepository
from services.auth_service import AuthService
from db import get_db

usuario_controller = APIRouter()

def get_usr_service():
    return UsuarioService(UsuarioRepository(), AuthService())

@usuario_controller.post("/", response_model=UsuarioResponse)
def create_usuario(
    data: UsuarioCreate, 
    rol_basico_id: int, 
    db: Session = Depends(get_db), 
    svc: UsuarioService = Depends(get_usr_service)
):
    try:
        return svc.create_usuario(db, data, rol_basico_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@usuario_controller.patch("/{usuario_id}/perfil", response_model=UsuarioResponse)
def update_perfil(
    usuario_id: int, 
    data: UsuarioUpdate, 
    db: Session = Depends(get_db), 
    svc: UsuarioService = Depends(get_usr_service)
):
    try:
        return svc.update_perfil(db, usuario_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@usuario_controller.delete("/{usuario_id}")
def inactivar_cuenta(
    usuario_id: int, 
    db: Session = Depends(get_db), 
    svc: UsuarioService = Depends(get_usr_service)
):
    try:
        svc.inactivar_cuenta(db, usuario_id)
        return {"message": "Desvinculación estricta completada. La cuenta yace congelada inactiva."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
