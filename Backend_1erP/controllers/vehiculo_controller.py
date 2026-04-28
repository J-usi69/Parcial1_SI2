from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.vehiculo import VehiculoCreate, VehiculoResponse, VehiculoUpdate
from services.vehiculo_service import VehiculoService
from repositories.vehiculo_repository import VehiculoRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

vehiculo_controller = APIRouter()

def get_vehiculo_service():
    return VehiculoService(VehiculoRepository())

@vehiculo_controller.get("/", response_model=list[VehiculoResponse], dependencies=[Depends(require_permissions(["ver_vehiculo"]))])
def get_vehiculos(db: Session = Depends(get_db), svc: VehiculoService = Depends(get_vehiculo_service), current_user=Depends(get_current_user)):
    return svc.get_vehiculos(db, current_user)

@vehiculo_controller.get("/{vehiculo_id}", response_model=VehiculoResponse, dependencies=[Depends(require_permissions(["ver_vehiculo"]))])
def get_vehiculo(vehiculo_id: int, db: Session = Depends(get_db), svc: VehiculoService = Depends(get_vehiculo_service), current_user=Depends(get_current_user)):
    try:
        return svc.get_vehiculo(db, vehiculo_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@vehiculo_controller.post("/", response_model=VehiculoResponse, dependencies=[Depends(require_permissions(["crear_vehiculo"]))])
def create_vehiculo(data: VehiculoCreate, db: Session = Depends(get_db), svc: VehiculoService = Depends(get_vehiculo_service), current_user=Depends(get_current_user)):
    try:
        return svc.create_vehiculo(db, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@vehiculo_controller.patch("/{vehiculo_id}", response_model=VehiculoResponse, dependencies=[Depends(require_permissions(["editar_vehiculo"]))])
def update_vehiculo(vehiculo_id: int, data: VehiculoUpdate, db: Session = Depends(get_db), svc: VehiculoService = Depends(get_vehiculo_service), current_user=Depends(get_current_user)):
    try:
        return svc.update_vehiculo(db, vehiculo_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@vehiculo_controller.delete("/{vehiculo_id}", dependencies=[Depends(require_permissions(["inactivar_vehiculo"]))])
def inactivar_vehiculo(vehiculo_id: int, db: Session = Depends(get_db), svc: VehiculoService = Depends(get_vehiculo_service), current_user=Depends(get_current_user)):
    try:
        svc.inactivar_vehiculo(db, vehiculo_id, current_user)
        return {"message": "Vehículo inactivado correctamente."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
