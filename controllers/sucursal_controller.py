from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.sucursal import SucursalCreate, SucursalResponse, SucursalUpdate
from services.sucursal_service import SucursalService
from repositories.sucursal_repository import SucursalRepository
from db import get_db

sucursal_controller = APIRouter()

def get_sucursal_service():
    return SucursalService(SucursalRepository())

@sucursal_controller.get("/", response_model=list[SucursalResponse])
def get_sucursales(db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service)):
    return svc.get_sucursales(db)

@sucursal_controller.get("/{sucursal_id}", response_model=SucursalResponse)
def get_sucursal(sucursal_id: int, db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service)):
    try:
        return svc.get_sucursal(db, sucursal_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@sucursal_controller.get("/empresa/{empresa_id}", response_model=list[SucursalResponse])
def get_sucursales_por_empresa(empresa_id: int, db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service)):
    return svc.get_by_empresa(db, empresa_id)

@sucursal_controller.post("/", response_model=SucursalResponse)
def create_sucursal(data: SucursalCreate, db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service)):
    return svc.create_sucursal(db, data)

@sucursal_controller.patch("/{sucursal_id}", response_model=SucursalResponse)
def update_sucursal(sucursal_id: int, data: SucursalUpdate, db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service)):
    try:
        return svc.update_sucursal(db, sucursal_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@sucursal_controller.delete("/{sucursal_id}")
def delete_sucursal(sucursal_id: int, db: Session = Depends(get_db), svc: SucursalService = Depends(get_sucursal_service)):
    try:
        svc.soft_delete_sucursal(db, sucursal_id)
        return {"message": "Extirpación operativa lograda: La Sucursal ha sido transicionada al estado inactivo."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
