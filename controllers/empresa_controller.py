from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.empresa import EmpresaCreate, EmpresaResponse, EmpresaUpdate
from services.empresa_service import EmpresaService
from repositories.empresa_repository import EmpresaRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

empresa_controller = APIRouter()

def get_empresa_service():
    return EmpresaService(EmpresaRepository())

@empresa_controller.get("/", response_model=list[EmpresaResponse], dependencies=[Depends(require_permissions(["ver_empresa"]))])
def get_empresas(db: Session = Depends(get_db), svc: EmpresaService = Depends(get_empresa_service), current_user = Depends(get_current_user)):
    return svc.get_empresas(db, current_user)

@empresa_controller.get("/{empresa_id}", response_model=EmpresaResponse, dependencies=[Depends(require_permissions(["ver_empresa"]))])
def get_empresa(empresa_id: int, db: Session = Depends(get_db), svc: EmpresaService = Depends(get_empresa_service), current_user = Depends(get_current_user)):
    try:
        return svc.get_empresa(db, empresa_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@empresa_controller.post("/", response_model=EmpresaResponse, dependencies=[Depends(require_permissions(["crear_empresa"]))])
def create_empresa(data: EmpresaCreate, db: Session = Depends(get_db), svc: EmpresaService = Depends(get_empresa_service), current_user = Depends(get_current_user)):
    if not current_user.is_staff:
        raise HTTPException(status_code=403, detail="La creación manual de empresas está reservada para el SuperUsuario. Los administradores deben usar el onboarding de taller.")
    try:
        return svc.create_empresa(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@empresa_controller.patch("/{empresa_id}", response_model=EmpresaResponse, dependencies=[Depends(require_permissions(["editar_empresa"]))])
def update_empresa(empresa_id: int, data: EmpresaUpdate, db: Session = Depends(get_db), svc: EmpresaService = Depends(get_empresa_service), current_user = Depends(get_current_user)):
    try:
        return svc.update_empresa(db, empresa_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@empresa_controller.delete("/{empresa_id}", dependencies=[Depends(require_permissions(["inactivar_empresa"]))])
def delete_empresa(empresa_id: int, db: Session = Depends(get_db), svc: EmpresaService = Depends(get_empresa_service), current_user = Depends(get_current_user)):
    try:
        svc.soft_delete_empresa(db, empresa_id, current_user)
        return {"message": "La empresa ha sido transicionada al estado inactivo."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
