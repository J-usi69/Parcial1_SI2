from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.suscripcion import SuscripcionCreate, SuscripcionResponse, SuscripcionUpdate
from services.suscripcion_service import SuscripcionService
from repositories.suscripcion_repository import SuscripcionRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

suscripcion_controller = APIRouter()

def get_suscripcion_service():
    return SuscripcionService(SuscripcionRepository())

@suscripcion_controller.post("/", response_model=SuscripcionResponse, dependencies=[Depends(require_permissions(["crear_suscripciones"]))])
def create_suscripcion(data: SuscripcionCreate, db: Session = Depends(get_db), svc: SuscripcionService = Depends(get_suscripcion_service)):
    try:
        return svc.create_suscripcion(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@suscripcion_controller.get("/", response_model=list[SuscripcionResponse], dependencies=[Depends(require_permissions(["ver_suscripciones"]))])
def get_suscripciones(db: Session = Depends(get_db), svc: SuscripcionService = Depends(get_suscripcion_service)):
    return svc.get_suscripciones(db)

@suscripcion_controller.patch("/{suscripcion_id}", response_model=SuscripcionResponse, dependencies=[Depends(require_permissions(["editar_suscripciones"]))])
def update_suscripcion(suscripcion_id: int, data: SuscripcionUpdate, db: Session = Depends(get_db), svc: SuscripcionService = Depends(get_suscripcion_service)):
    try:
        return svc.update_suscripcion(db, suscripcion_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@suscripcion_controller.delete("/{suscripcion_id}", dependencies=[Depends(require_permissions(["desactivar_suscripciones"]))])
def desactivar_suscripcion(suscripcion_id: int, db: Session = Depends(get_db), svc: SuscripcionService = Depends(get_suscripcion_service)):
    try:
        svc.desactivar_suscripcion(db, suscripcion_id)
        return {"message": "El plan de suscripción comercial ha sido transicionado formalmente a estado inactivo."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
