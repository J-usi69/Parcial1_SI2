from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from schemas.metodo_pago import MetodoPagoCreate, MetodoPagoUpdate, MetodoPagoResponse
from services.metodo_pago_service import MetodoPagoService
from repositories.metodo_pago_repository import MetodoPagoRepository
from services.auth_service import get_current_user, require_permissions

def get_mp_service():
    return MetodoPagoService(MetodoPagoRepository())

router = APIRouter(prefix="/metodos-pago", tags=["Métodos de Pago"])

@router.get("/propietario/{propietario_tipo}/{propietario_id}", response_model=List[MetodoPagoResponse])
def listar_metodos_pago(
    propietario_tipo: str,
    propietario_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_metodo_pago"])),
    service: MetodoPagoService = Depends(get_mp_service)
):
    try:
        return service.get_por_propietario(db, propietario_tipo, propietario_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.post("/", response_model=MetodoPagoResponse)
def crear_metodo_pago(
    data: MetodoPagoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["crear_metodo_pago"])),
    service: MetodoPagoService = Depends(get_mp_service)
):
    try:
        return service.create_metodo(db, data, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{metodo_id}", response_model=MetodoPagoResponse)
def editar_metodo_pago(
    metodo_id: int,
    data: MetodoPagoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["editar_metodo_pago"])),
    service: MetodoPagoService = Depends(get_mp_service)
):
    try:
        return service.update_metodo(db, metodo_id, data, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{metodo_id}")
def inactivar_metodo_pago(
    metodo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["inactivar_metodo_pago"])),
    service: MetodoPagoService = Depends(get_mp_service)
):
    try:
        service.inactivar_metodo(db, metodo_id, current_user)
        return {"mensaje": "Método de pago inactivado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
