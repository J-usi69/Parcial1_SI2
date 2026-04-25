from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.rol_permiso import RolPermisoCreate, RolPermisoResponse, RolPermisoUpdate
from services.rol_permiso_service import RolPermisoService
from repositories.rol_permiso_repository import RolPermisoRepository
from db import get_db

rol_permiso_controller = APIRouter()

def get_rpc_service():
    return RolPermisoService(RolPermisoRepository())

@rol_permiso_controller.post("/", response_model=RolPermisoResponse)
def asignar_permiso(data: RolPermisoCreate, db: Session = Depends(get_db), svc: RolPermisoService = Depends(get_rpc_service)):
    try:
        return svc.asignar_permiso(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@rol_permiso_controller.patch("/{rol_id}/permiso/{permiso_id}/vigencia", response_model=RolPermisoResponse)
def actualizar_vigencia(
    rol_id: int, 
    permiso_id: int, 
    data: RolPermisoUpdate,
    db: Session = Depends(get_db), 
    svc: RolPermisoService = Depends(get_rpc_service)
):
    try:
        return svc.update_vigencia(db, rol_id, permiso_id, data.vigente)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@rol_permiso_controller.get("/rol/{rol_id}", response_model=list[RolPermisoResponse])
def get_permisos(rol_id: int, db: Session = Depends(get_db), svc: RolPermisoService = Depends(get_rpc_service)):
    return svc.get_permisos_by_rol(db, rol_id)
