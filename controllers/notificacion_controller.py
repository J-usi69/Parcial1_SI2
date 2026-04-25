from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.notificacion import NotificacionCreate, NotificacionResponse
from services.notificacion_service import NotificacionService
from repositories.notificacion_repository import NotificacionRepository
from repositories.usuario_repository import UsuarioRepository
from db import get_db

notificacion_controller = APIRouter()

def get_notificacion_service():
    return NotificacionService(NotificacionRepository(), UsuarioRepository())

@notificacion_controller.post("/", response_model=NotificacionResponse)
def create_notificacion(
    data: NotificacionCreate, 
    db: Session = Depends(get_db), 
    svc: NotificacionService = Depends(get_notificacion_service)
):
    try:
        return svc.create_notificacion(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
