from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.rol_usuario import RolUsuarioCreate, RolUsuarioResponse
from services.rol_usuario_service import RolUsuarioService
from repositories.rol_usuario_repository import RolUsuarioRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

rol_usuario_controller = APIRouter()

def get_ru_service():
    return RolUsuarioService(RolUsuarioRepository())

@rol_usuario_controller.post("/", response_model=RolUsuarioResponse, dependencies=[Depends(require_permissions(["asignar_rol"]))])
def asignar_rol(data: RolUsuarioCreate, db: Session = Depends(get_db), svc: RolUsuarioService = Depends(get_ru_service), current_user = Depends(get_current_user)):
    try:
        return svc.asignar_rol(db, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@rol_usuario_controller.delete("/{rol_id}/usuario/{usuario_id}", dependencies=[Depends(require_permissions(["revocar_rol"]))])
def revocar_rol(rol_id: int, usuario_id: int, db: Session = Depends(get_db), svc: RolUsuarioService = Depends(get_ru_service), current_user = Depends(get_current_user)):
    try:
        svc.revocar_rol(db, rol_id, usuario_id, current_user)
        return {"message": "Extirpación exitosa. El rol ha sido desvinculado orgánicamente del usuario."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@rol_usuario_controller.get("/usuario/{usuario_id}", response_model=list[RolUsuarioResponse], dependencies=[Depends(require_permissions(["ver_usuario"]))])
def get_roles_by_usuario(usuario_id: int, db: Session = Depends(get_db), svc: RolUsuarioService = Depends(get_ru_service), current_user = Depends(get_current_user)):
    try:
        return svc.get_roles_by_usuario(db, usuario_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
