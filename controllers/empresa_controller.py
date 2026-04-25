from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.empresa import EmpresaCreate, EmpresaResponse, EmpresaUpdate
from services.empresa_service import EmpresaService
from repositories.empresa_repository import EmpresaRepository
from db import get_db

empresa_controller = APIRouter()

def get_empresa_service():
    return EmpresaService(EmpresaRepository())

@empresa_controller.get("/", response_model=list[EmpresaResponse])
def get_empresas(db: Session = Depends(get_db), svc: EmpresaService = Depends(get_empresa_service)):
    return svc.get_empresas(db)

@empresa_controller.get("/{empresa_id}", response_model=EmpresaResponse)
def get_empresa(empresa_id: int, db: Session = Depends(get_db), svc: EmpresaService = Depends(get_empresa_service)):
    try:
        return svc.get_empresa(db, empresa_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@empresa_controller.post("/", response_model=EmpresaResponse)
def create_empresa(data: EmpresaCreate, db: Session = Depends(get_db), svc: EmpresaService = Depends(get_empresa_service)):
    try:
        return svc.create_empresa(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@empresa_controller.patch("/{empresa_id}", response_model=EmpresaResponse)
def update_empresa(empresa_id: int, data: EmpresaUpdate, db: Session = Depends(get_db), svc: EmpresaService = Depends(get_empresa_service)):
    try:
        return svc.update_empresa(db, empresa_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@empresa_controller.delete("/{empresa_id}")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db), svc: EmpresaService = Depends(get_empresa_service)):
    try:
        svc.soft_delete_empresa(db, empresa_id)
        return {"message": "La empresa ha sido transicionada al estado inactivo."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
