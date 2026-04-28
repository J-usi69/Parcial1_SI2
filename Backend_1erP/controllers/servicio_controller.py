from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.servicio import ServicioCreate, ServicioResponse, ServicioUpdate
from services.servicio_service import ServicioService
from repositories.servicio_repository import ServicioRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

servicio_controller = APIRouter()

def get_servicio_service():
    return ServicioService(ServicioRepository())

@servicio_controller.get("/", response_model=list[ServicioResponse], dependencies=[Depends(require_permissions(["ver_servicio"]))])
def get_servicios(db: Session = Depends(get_db), svc: ServicioService = Depends(get_servicio_service), current_user=Depends(get_current_user)):
    return svc.get_servicios(db, current_user)

@servicio_controller.get("/{servicio_id}", response_model=ServicioResponse, dependencies=[Depends(require_permissions(["ver_servicio"]))])
def get_servicio(servicio_id: int, db: Session = Depends(get_db), svc: ServicioService = Depends(get_servicio_service), current_user=Depends(get_current_user)):
    try:
        return svc.get_servicio(db, servicio_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@servicio_controller.post("/", response_model=ServicioResponse, dependencies=[Depends(require_permissions(["crear_servicio"]))])
def create_servicio(data: ServicioCreate, db: Session = Depends(get_db), svc: ServicioService = Depends(get_servicio_service), current_user=Depends(get_current_user)):
    try:
        return svc.create_servicio(db, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@servicio_controller.patch("/{servicio_id}", response_model=ServicioResponse, dependencies=[Depends(require_permissions(["editar_servicio"]))])
def update_servicio(servicio_id: int, data: ServicioUpdate, db: Session = Depends(get_db), svc: ServicioService = Depends(get_servicio_service), current_user=Depends(get_current_user)):
    try:
        return svc.update_servicio(db, servicio_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@servicio_controller.delete("/{servicio_id}", dependencies=[Depends(require_permissions(["inactivar_servicio"]))])
def inactivar_servicio(servicio_id: int, db: Session = Depends(get_db), svc: ServicioService = Depends(get_servicio_service), current_user=Depends(get_current_user)):
    try:
        svc.inactivar_servicio(db, servicio_id, current_user)
        return {"message": "Servicio inactivado correctamente."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
