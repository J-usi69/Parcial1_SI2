from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.sucursal import SucursalCreate, SucursalResponse, SucursalUpdate
from services.sucursal_service import SucursalService
from repositories.sucursal_repository import SucursalRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

sucursal_controller = APIRouter()

def get_sucursal_service():
    return SucursalService(SucursalRepository())

@sucursal_controller.get("/", response_model=list[SucursalResponse], dependencies=[Depends(require_permissions(["ver_sucursal"]))])
def get_sucursales(db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service), current_user = Depends(get_current_user)):
    return svc.get_sucursales(db, current_user)

@sucursal_controller.get("/{sucursal_id}", response_model=SucursalResponse, dependencies=[Depends(require_permissions(["ver_sucursal"]))])
def get_sucursal(sucursal_id: int, db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service), current_user = Depends(get_current_user)):
    try:
        return svc.get_sucursal(db, sucursal_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@sucursal_controller.get("/empresa/{empresa_id}", response_model=list[SucursalResponse], dependencies=[Depends(require_permissions(["ver_sucursal"]))])
def get_sucursales_por_empresa(empresa_id: int, db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service), current_user = Depends(get_current_user)):
    try:
        return svc.get_by_empresa(db, empresa_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@sucursal_controller.post("/", response_model=SucursalResponse, dependencies=[Depends(require_permissions(["crear_sucursal"]))])
def create_sucursal(data: SucursalCreate, db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service), current_user = Depends(get_current_user)):
    try:
        return svc.create_sucursal(db, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@sucursal_controller.patch("/{sucursal_id}", response_model=SucursalResponse, dependencies=[Depends(require_permissions(["editar_sucursal"]))])
def update_sucursal(sucursal_id: int, data: SucursalUpdate, db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service), current_user = Depends(get_current_user)):
    try:
        return svc.update_sucursal(db, sucursal_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@sucursal_controller.delete("/{sucursal_id}", dependencies=[Depends(require_permissions(["inactivar_sucursal"]))])
def delete_sucursal(sucursal_id: int, db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service), current_user = Depends(get_current_user)):
    try:
        svc.soft_delete_sucursal(db, sucursal_id, current_user)
        return {"message": "Extirpación operativa lograda: La Sucursal ha sido transicionada al estado inactivo."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
