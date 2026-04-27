from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.notificacion import NotificacionCreate, NotificacionResponse
from services.notificacion_service import NotificacionService
from repositories.notificacion_repository import NotificacionRepository
from repositories.usuario_repository import UsuarioRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

notificacion_controller = APIRouter()

def get_notificacion_service():
    return NotificacionService(NotificacionRepository(), UsuarioRepository())

@notificacion_controller.get("/", response_model=list[NotificacionResponse], dependencies=[Depends(require_permissions(["ver_notificacion"]))])
def get_notificaciones(db: Session = Depends(get_db), svc: NotificacionService = Depends(get_notificacion_service)):
    return svc.get_notificaciones(db)

@notificacion_controller.get("/{notificacion_id}", response_model=NotificacionResponse, dependencies=[Depends(require_permissions(["ver_notificacion"]))])
def get_notificacion(notificacion_id: int, db: Session = Depends(get_db), svc: NotificacionService = Depends(get_notificacion_service)):
    try:
        return svc.get_notificacion_by_id(db, notificacion_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@notificacion_controller.post("/", response_model=NotificacionResponse, dependencies=[Depends(require_permissions(["crear_notificacion"]))])
def create_notificacion(
    data: NotificacionCreate, 
    db: Session = Depends(get_db), 
    svc: NotificacionService = Depends(get_notificacion_service)
):
    try:
        return svc.create_notificacion(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
