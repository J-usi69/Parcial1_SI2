from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.permiso import PermisoCreate, PermisoResponse, PermisoUpdate
from services.permiso_service import PermisoService
from repositories.permiso_repository import PermisoRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

permiso_controller = APIRouter()

def get_pm_service():
    return PermisoService(PermisoRepository())

@permiso_controller.get("/", response_model=list[PermisoResponse], dependencies=[Depends(require_permissions(["ver_permisos"]))])
def get_permisos(db: Session = Depends(get_db), svc: PermisoService = Depends(get_pm_service)):
    return svc.get_permisos(db)

@permiso_controller.post("/", response_model=PermisoResponse, dependencies=[Depends(require_permissions(["crear_permisos"]))])
def create_permiso(data: PermisoCreate, db: Session = Depends(get_db), svc: PermisoService = Depends(get_pm_service)):
    try:
        return svc.create_permiso(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@permiso_controller.patch("/{permiso_id}", response_model=PermisoResponse, dependencies=[Depends(require_permissions(["editar_permisos"]))])
def update_permiso(permiso_id: int, data: PermisoUpdate, db: Session = Depends(get_db), svc: PermisoService = Depends(get_pm_service)):
    try:
        return svc.update_permiso(db, permiso_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@permiso_controller.delete("/{permiso_id}", dependencies=[Depends(require_permissions(["eliminar_permisos"]))])
def delete_permiso(permiso_id: int, db: Session = Depends(get_db), svc: PermisoService = Depends(get_pm_service)):
    try:
        svc.delete_permiso(db, permiso_id)
        return {"message": "El modelo relacional fundamental del permiso ha sido seccionado exitosamente."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
