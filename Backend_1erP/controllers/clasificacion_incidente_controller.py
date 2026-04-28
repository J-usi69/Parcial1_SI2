from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from schemas.clasificacion_incidente import ClasificacionIncidenteResponse, ClasificacionIncidenteReport, ClasificacionIncidenteRevalidate
from services.clasificacion_incidente_service import ClasificacionIncidenteService
from repositories.clasificacion_incidente_repository import ClasificacionIncidenteRepository
from services.auth_service import get_current_user, require_permissions

def get_clasif_service():
    return ClasificacionIncidenteService(ClasificacionIncidenteRepository())

router = APIRouter(prefix="/clasificaciones", tags=["Clasificación IA"])

@router.get("/solicitud/{solicitud_id}", response_model=List[ClasificacionIncidenteResponse])
def listar_clasificaciones(
    solicitud_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_clasificacion_incidente"])),
    service: ClasificacionIncidenteService = Depends(get_clasif_service)
):
    try:
        return service.get_por_solicitud(db, solicitud_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.post("/{clasificacion_id}/reportar", response_model=ClasificacionIncidenteResponse)
def reportar_clasificacion(
    clasificacion_id: int,
    data: ClasificacionIncidenteReport,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["reportar_clasificacion_incidente"])),
    service: ClasificacionIncidenteService = Depends(get_clasif_service)
):
    try:
        return service.reportar_incorrecta(db, clasificacion_id, data, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{clasificacion_id}/revalidar", response_model=ClasificacionIncidenteResponse)
def revalidar_clasificacion(
    clasificacion_id: int,
    data: ClasificacionIncidenteRevalidate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["revalidar_clasificacion_incidente"])),
    service: ClasificacionIncidenteService = Depends(get_clasif_service)
):
    try:
        return service.revalidar(db, clasificacion_id, data, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Nota: El endpoint de creación inicial lo maneja el flujo interno o puede estar protegido
