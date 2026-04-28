from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.asignacion import AsignacionCreate, AsignacionResponse, AsignacionResponder
from services.asignacion_service import AsignacionService
from repositories.asignacion_repository import AsignacionRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

asignacion_controller = APIRouter()

def get_asignacion_service():
    return AsignacionService(AsignacionRepository())

@asignacion_controller.get("/", response_model=list[AsignacionResponse], dependencies=[Depends(require_permissions(["ver_asignacion"]))])
def get_asignaciones(db: Session = Depends(get_db), svc: AsignacionService = Depends(get_asignacion_service), current_user=Depends(get_current_user)):
    return svc.get_asignaciones(db, current_user)

@asignacion_controller.get("/{asignacion_id}", response_model=AsignacionResponse, dependencies=[Depends(require_permissions(["ver_asignacion"]))])
def get_asignacion(asignacion_id: int, db: Session = Depends(get_db), svc: AsignacionService = Depends(get_asignacion_service), current_user=Depends(get_current_user)):
    try:
        return svc.get_asignacion(db, asignacion_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@asignacion_controller.post("/", response_model=AsignacionResponse, dependencies=[Depends(require_permissions(["crear_asignacion"]))])
def crear_asignacion(data: AsignacionCreate, db: Session = Depends(get_db), svc: AsignacionService = Depends(get_asignacion_service), current_user=Depends(get_current_user)):
    try:
        return svc.crear_asignacion(db, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@asignacion_controller.patch("/{asignacion_id}/responder", response_model=AsignacionResponse, dependencies=[Depends(require_permissions(["responder_asignacion"]))])
def responder_asignacion(asignacion_id: int, data: AsignacionResponder, db: Session = Depends(get_db), svc: AsignacionService = Depends(get_asignacion_service), current_user=Depends(get_current_user)):
    try:
        return svc.responder_asignacion(db, asignacion_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
