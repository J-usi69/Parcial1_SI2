from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.solicitud import SolicitudCreate, SolicitudResponse, SolicitudUpdate
from services.solicitud_service import SolicitudService
from repositories.solicitud_repository import SolicitudRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db
from typing import Optional

solicitud_controller = APIRouter()

def get_solicitud_service():
    return SolicitudService(SolicitudRepository())

@solicitud_controller.get("/", response_model=list[SolicitudResponse], dependencies=[Depends(require_permissions(["ver_solicitud"]))])
def get_solicitudes(db: Session = Depends(get_db), svc: SolicitudService = Depends(get_solicitud_service), current_user=Depends(get_current_user)):
    return svc.get_solicitudes(db, current_user)

@solicitud_controller.get("/{solicitud_id}", response_model=SolicitudResponse, dependencies=[Depends(require_permissions(["ver_solicitud"]))])
def get_solicitud(solicitud_id: int, db: Session = Depends(get_db), svc: SolicitudService = Depends(get_solicitud_service), current_user=Depends(get_current_user)):
    try:
        return svc.get_solicitud(db, solicitud_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@solicitud_controller.post("/", response_model=SolicitudResponse, dependencies=[Depends(require_permissions(["crear_solicitud"]))])
def create_solicitud(data: SolicitudCreate, db: Session = Depends(get_db), svc: SolicitudService = Depends(get_solicitud_service), current_user=Depends(get_current_user)):
    try:
        return svc.create_solicitud(db, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_controller.patch("/{solicitud_id}/estado", response_model=SolicitudResponse, dependencies=[Depends(require_permissions(["actualizar_estado_servicio"]))])
def actualizar_estado(solicitud_id: int, data: SolicitudUpdate, db: Session = Depends(get_db), svc: SolicitudService = Depends(get_solicitud_service), current_user=Depends(get_current_user)):
    try:
        return svc.actualizar_estado(db, solicitud_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_controller.patch("/{solicitud_id}/decidir", response_model=SolicitudResponse, dependencies=[Depends(require_permissions(["decidir_solicitud"]))])
def decidir_solicitud(solicitud_id: int, data: SolicitudUpdate, db: Session = Depends(get_db), svc: SolicitudService = Depends(get_solicitud_service), current_user=Depends(get_current_user)):
    try:
        return svc.actualizar_estado(db, solicitud_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_controller.patch("/{solicitud_id}/cancelar", response_model=SolicitudResponse, dependencies=[Depends(require_permissions(["cancelar_solicitud"]))])
def cancelar_solicitud(solicitud_id: int, motivo: Optional[str] = None, db: Session = Depends(get_db), svc: SolicitudService = Depends(get_solicitud_service), current_user=Depends(get_current_user)):
    try:
        return svc.cancelar_solicitud(db, solicitud_id, motivo or "", current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
