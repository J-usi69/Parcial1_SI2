from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.notificacion_usuario import NotificacionUsuarioCreate, NotificacionUsuarioResponse
from services.notificacion_usuario_service import NotificacionUsuarioService
from repositories.notificacion_usuario_repository import NotificacionUsuarioRepository
from repositories.notificacion_repository import NotificacionRepository
from repositories.usuario_repository import UsuarioRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

notificacion_usuario_controller = APIRouter()

def get_notif_usu_service():
    return NotificacionUsuarioService(
        NotificacionUsuarioRepository(),
        NotificacionRepository(),
        UsuarioRepository()
    )

@notificacion_usuario_controller.post("/", response_model=NotificacionUsuarioResponse, dependencies=[Depends(require_permissions(["crear_notificacion"]))])
def asignar_notificacion(
    data: NotificacionUsuarioCreate, 
    db: Session = Depends(get_db), 
    svc: NotificacionUsuarioService = Depends(get_notif_usu_service)
):
    try:
        return svc.asignar_destinatario(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@notificacion_usuario_controller.patch("/{notificacion_id}/usuario/{usuario_id}/leido", response_model=NotificacionUsuarioResponse, dependencies=[Depends(require_permissions(["marcar_notificacion_leida"]))])
def marcar_como_leido(
    notificacion_id: int, 
    usuario_id: int,
    db: Session = Depends(get_db), 
    svc: NotificacionUsuarioService = Depends(get_notif_usu_service),
    current_user = Depends(get_current_user)
):
    if not current_user.is_staff and current_user.id != usuario_id:
        raise HTTPException(status_code=403, detail="Violación de Ámbito: No puede marcar como leída una notificación de otro usuario.")
    try:
        return svc.marcar_leido(db, usuario_id, notificacion_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@notificacion_usuario_controller.get("/usuario/{usuario_id}/mis-notificaciones", response_model=list[NotificacionUsuarioResponse], dependencies=[Depends(require_permissions(["ver_notificacion"]))])
def get_mis_notificaciones(
    usuario_id: int,
    db: Session = Depends(get_db), 
    svc: NotificacionUsuarioService = Depends(get_notif_usu_service),
    current_user = Depends(get_current_user)
):
    if not current_user.is_staff and current_user.id != usuario_id:
        raise HTTPException(status_code=403, detail="Violación de Ámbito: No puede leer las notificaciones de otro usuario.")
    return svc.get_mis_notificaciones(db, usuario_id)

