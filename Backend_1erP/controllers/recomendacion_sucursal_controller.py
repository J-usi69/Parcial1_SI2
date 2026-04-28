from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from schemas.recomendacion_sucursal import RecomendacionSucursalResponse
from services.recomendacion_sucursal_service import RecomendacionSucursalService
from repositories.recomendacion_sucursal_repository import RecomendacionSucursalRepository
from services.auth_service import get_current_user, require_permissions

def get_recom_service():
    return RecomendacionSucursalService(RecomendacionSucursalRepository())

router = APIRouter(prefix="/recomendaciones", tags=["Recomendación Sucursal"])

@router.get("/solicitud/{solicitud_id}", response_model=List[RecomendacionSucursalResponse])
def listar_recomendaciones(
    solicitud_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_recomendacion_sucursal"])),
    service: RecomendacionSucursalService = Depends(get_recom_service)
):
    try:
        return service.get_por_solicitud(db, solicitud_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.post("/solicitud/{solicitud_id}/recalcular", response_model=List[RecomendacionSucursalResponse])
def recalcular_recomendacion(
    solicitud_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["recalcular_recomendacion_sucursal"])),
    service: RecomendacionSucursalService = Depends(get_recom_service)
):
    try:
        return service.recalcular_recomendacion(db, solicitud_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
