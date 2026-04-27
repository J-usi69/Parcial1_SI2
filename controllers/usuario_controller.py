from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from services.usuario_service import UsuarioService
from repositories.usuario_repository import UsuarioRepository
from services.auth_service import AuthService, get_current_user, require_permissions
from db import get_db

usuario_controller = APIRouter()

def get_usr_service():
    return UsuarioService(UsuarioRepository(), AuthService())

@usuario_controller.get("/", response_model=list[UsuarioResponse], dependencies=[Depends(require_permissions(["ver_usuario"]))])
def get_usuarios(db: Session = Depends(get_db), svc: UsuarioService = Depends(get_usr_service), current_user = Depends(get_current_user)):
    return svc.get_usuarios(db, current_user)

@usuario_controller.get("/{usuario_id}", response_model=UsuarioResponse, dependencies=[Depends(require_permissions(["ver_usuario"]))])
def get_usuario(usuario_id: int, db: Session = Depends(get_db), svc: UsuarioService = Depends(get_usr_service), current_user = Depends(get_current_user)):
    try:
        return svc.get_usuario_by_id(db, usuario_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@usuario_controller.post("/", response_model=UsuarioResponse, dependencies=[Depends(require_permissions(["crear_usuario"]))])
def create_usuario(
    data: UsuarioCreate, 
    rol_basico_id: int, 
    db: Session = Depends(get_db), 
    svc: UsuarioService = Depends(get_usr_service),
    current_user = Depends(get_current_user)
):
    try:
        return svc.create_usuario(db, data, rol_basico_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@usuario_controller.patch("/{usuario_id}/perfil", response_model=UsuarioResponse, dependencies=[Depends(require_permissions(["editar_usuario"]))])
def update_perfil(
    usuario_id: int, 
    data: UsuarioUpdate, 
    db: Session = Depends(get_db), 
    svc: UsuarioService = Depends(get_usr_service),
    current_user = Depends(get_current_user)
):
    try:
        return svc.update_perfil(db, usuario_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@usuario_controller.patch("/{usuario_id}/inactivar", dependencies=[Depends(require_permissions(["inactivar_usuario"]))])
def inactivar_cuenta(
    usuario_id: int, 
    db: Session = Depends(get_db), 
    svc: UsuarioService = Depends(get_usr_service),
    current_user = Depends(get_current_user)
):
    try:
        svc.inactivar_cuenta(db, usuario_id, current_user)
        return {"message": "Desvinculación estricta completada. La cuenta yace congelada inactiva."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
