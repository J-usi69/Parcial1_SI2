from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from schemas.pago import PagoCreate, PagoUpdate, PagoVerify, PagoResponse
from services.pago_service import PagoService
from repositories.pago_repository import PagoRepository
from services.auth_service import get_current_user, require_permissions

def get_pago_service():
    return PagoService(PagoRepository())

router = APIRouter(prefix="/pagos", tags=["Pagos"])

@router.get("/solicitud/{solicitud_id}", response_model=PagoResponse)
def obtener_pago_solicitud(
    solicitud_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_pago"])),
    service: PagoService = Depends(get_pago_service)
):
    try:
        pago = service.get_por_solicitud(db, solicitud_id, current_user)
        if not pago:
            raise HTTPException(status_code=404, detail="No hay pago registrado para esta solicitud.")
        return pago
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/cliente/{cliente_id}", response_model=List[PagoResponse])
def obtener_pagos_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_pago"])),
    service: PagoService = Depends(get_pago_service)
):
    try:
        return service.get_pagos_cliente(db, cliente_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/empresa/{empresa_id}", response_model=List[PagoResponse])
def obtener_pagos_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_pago"])),
    service: PagoService = Depends(get_pago_service)
):
    try:
        return service.get_pagos_empresa(db, empresa_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=PagoResponse)
def registrar_pago(
    data: PagoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["crear_pago"])),
    service: PagoService = Depends(get_pago_service)
):
    try:
        return service.create_pago(db, data, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{pago_id}", response_model=PagoResponse)
def actualizar_estado_pago(
    pago_id: int,
    data: PagoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["editar_pago"])),
    service: PagoService = Depends(get_pago_service)
):
    try:
        return service.update_estado(db, pago_id, data, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{pago_id}/verificar", response_model=PagoResponse)
def verificar_pago(
    pago_id: int,
    data: PagoVerify,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["verificar_pago"])),
    service: PagoService = Depends(get_pago_service)
):
    try:
        return service.verificar_pago(db, pago_id, data, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
