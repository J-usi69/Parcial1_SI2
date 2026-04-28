from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.diagnostico import DiagnosticoCreate, DiagnosticoResponse, DiagnosticoUpdate
from services.diagnostico_service import DiagnosticoService
from repositories.diagnostico_repository import DiagnosticoRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

diagnostico_controller = APIRouter()

def get_diagnostico_service():
    return DiagnosticoService(DiagnosticoRepository())

@diagnostico_controller.get("/{diagnostico_id}", response_model=DiagnosticoResponse, dependencies=[Depends(require_permissions(["ver_diagnostico"]))])
def get_diagnostico(diagnostico_id: int, db: Session = Depends(get_db), svc: DiagnosticoService = Depends(get_diagnostico_service), current_user=Depends(get_current_user)):
    try:
        return svc.get_diagnostico(db, diagnostico_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@diagnostico_controller.get("/asignacion/{asignacion_id}", response_model=DiagnosticoResponse, dependencies=[Depends(require_permissions(["ver_diagnostico"]))])
def get_por_asignacion(asignacion_id: int, db: Session = Depends(get_db), svc: DiagnosticoService = Depends(get_diagnostico_service), current_user=Depends(get_current_user)):
    try:
        return svc.get_por_asignacion(db, asignacion_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@diagnostico_controller.post("/", response_model=DiagnosticoResponse, dependencies=[Depends(require_permissions(["crear_diagnostico"]))])
def create_diagnostico(data: DiagnosticoCreate, db: Session = Depends(get_db), svc: DiagnosticoService = Depends(get_diagnostico_service), current_user=Depends(get_current_user)):
    try:
        return svc.create_diagnostico(db, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@diagnostico_controller.patch("/{diagnostico_id}", response_model=DiagnosticoResponse, dependencies=[Depends(require_permissions(["editar_diagnostico"]))])
def update_diagnostico(diagnostico_id: int, data: DiagnosticoUpdate, db: Session = Depends(get_db), svc: DiagnosticoService = Depends(get_diagnostico_service), current_user=Depends(get_current_user)):
    try:
        return svc.update_diagnostico(db, diagnostico_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
