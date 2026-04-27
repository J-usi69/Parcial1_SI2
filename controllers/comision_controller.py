from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from schemas.comision import ComisionResponse
from services.comision_service import ComisionService
from repositories.comision_repository import ComisionRepository
from services.auth_service import get_current_user, require_permissions

def get_comision_service():
    return ComisionService(ComisionRepository())

router = APIRouter(prefix="/comisiones", tags=["Comisiones"])

@router.get("/solicitud/{solicitud_id}", response_model=ComisionResponse)
def obtener_comision_solicitud(
    solicitud_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_comision"])),
    service: ComisionService = Depends(get_comision_service)
):
    try:
        comision = service.repository.get_by_solicitud(db, solicitud_id)
        if not comision:
            raise HTTPException(status_code=404, detail="Comisión no encontrada.")
        service._validate_scope(db, current_user, comision)
        return comision
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tecnico/{tecnico_id}", response_model=List[ComisionResponse])
def obtener_comisiones_tecnico(
    tecnico_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_comision"])),
    service: ComisionService = Depends(get_comision_service)
):
    try:
        return service.get_comisiones_tecnico(db, tecnico_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/empresa/{empresa_id}", response_model=List[ComisionResponse])
def obtener_comisiones_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_comision"])),
    service: ComisionService = Depends(get_comision_service)
):
    try:
        return service.get_comisiones_empresa(db, empresa_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{comision_id}/pagar", response_model=ComisionResponse)
def marcar_comision_pagada(
    comision_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["editar_comision"])),
    service: ComisionService = Depends(get_comision_service)
):
    try:
        return service.marcar_pagada(db, comision_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
