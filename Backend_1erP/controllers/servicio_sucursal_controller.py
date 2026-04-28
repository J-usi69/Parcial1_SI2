from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.servicio_sucursal import ServicioSucursalCreate, ServicioSucursalResponse, ServicioSucursalUpdate
from services.servicio_sucursal_service import ServicioSucursalService
from repositories.servicio_sucursal_repository import ServicioSucursalRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

servicio_sucursal_controller = APIRouter()

def get_ss_service():
    return ServicioSucursalService(ServicioSucursalRepository())

@servicio_sucursal_controller.get("/sucursal/{sucursal_id}", response_model=list[ServicioSucursalResponse], dependencies=[Depends(require_permissions(["ver_servicio_sucursal"]))])
def get_por_sucursal(sucursal_id: int, db: Session = Depends(get_db), svc: ServicioSucursalService = Depends(get_ss_service), current_user=Depends(get_current_user)):
    try:
        return svc.get_por_sucursal(db, sucursal_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@servicio_sucursal_controller.get("/{ss_id}", response_model=ServicioSucursalResponse, dependencies=[Depends(require_permissions(["ver_servicio_sucursal"]))])
def get_servicio_sucursal(ss_id: int, db: Session = Depends(get_db), svc: ServicioSucursalService = Depends(get_ss_service), current_user=Depends(get_current_user)):
    try:
        return svc.get_servicio_sucursal(db, ss_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@servicio_sucursal_controller.post("/", response_model=ServicioSucursalResponse, dependencies=[Depends(require_permissions(["asignar_servicio_sucursal"]))])
def asignar_servicio_sucursal(data: ServicioSucursalCreate, db: Session = Depends(get_db), svc: ServicioSucursalService = Depends(get_ss_service), current_user=Depends(get_current_user)):
    try:
        return svc.asignar(db, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@servicio_sucursal_controller.patch("/{ss_id}", response_model=ServicioSucursalResponse, dependencies=[Depends(require_permissions(["editar_servicio_sucursal"]))])
def editar_servicio_sucursal(ss_id: int, data: ServicioSucursalUpdate, db: Session = Depends(get_db), svc: ServicioSucursalService = Depends(get_ss_service), current_user=Depends(get_current_user)):
    try:
        return svc.editar(db, ss_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@servicio_sucursal_controller.delete("/{ss_id}", dependencies=[Depends(require_permissions(["inactivar_servicio_sucursal"]))])
def inactivar_servicio_sucursal(ss_id: int, db: Session = Depends(get_db), svc: ServicioSucursalService = Depends(get_ss_service), current_user=Depends(get_current_user)):
    try:
        svc.inactivar(db, ss_id, current_user)
        return {"message": "Servicio-Sucursal inactivado (disponible=False)."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
