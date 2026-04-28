from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.rol import RolCreate, RolResponse, RolUpdate
from services.rol_service import RolService
from repositories.rol_repository import RolRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

rol_controller = APIRouter()

def get_rol_service():
    return RolService(RolRepository())

@rol_controller.get("/", response_model=list[RolResponse], dependencies=[Depends(require_permissions(["ver_roles"]))])
def get_roles(db: Session = Depends(get_db), svc: RolService = Depends(get_rol_service)):
    return svc.get_roles(db)

@rol_controller.post("/", response_model=RolResponse, dependencies=[Depends(require_permissions(["crear_roles"]))])
def create_rol(data: RolCreate, db: Session = Depends(get_db), svc: RolService = Depends(get_rol_service)):
    try:
        return svc.create_rol(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@rol_controller.patch("/{rol_id}", response_model=RolResponse, dependencies=[Depends(require_permissions(["editar_roles"]))])
def update_rol(rol_id: int, data: RolUpdate, db: Session = Depends(get_db), svc: RolService = Depends(get_rol_service)):
    try:
        return svc.update_rol(db, rol_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@rol_controller.delete("/{rol_id}", dependencies=[Depends(require_permissions(["eliminar_roles"]))])
def delete_rol(rol_id: int, db: Session = Depends(get_db), svc: RolService = Depends(get_rol_service)):
    try:
        svc.delete_rol(db, rol_id)
        return {"message": "El modelo relacional ha sido podado de base de datos exitosamente."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
