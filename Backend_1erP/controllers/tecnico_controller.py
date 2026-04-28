from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.tecnico import TecnicoCreate, TecnicoResponse, TecnicoUpdate
from services.tecnico_service import TecnicoService
from repositories.tecnico_repository import TecnicoRepository
from services.auth_service import get_current_user, require_permissions
from db import get_db

tecnico_controller = APIRouter()

def get_tecnico_service():
    return TecnicoService(TecnicoRepository())

@tecnico_controller.get("/", response_model=list[TecnicoResponse], dependencies=[Depends(require_permissions(["ver_tecnico"]))])
def get_tecnicos(db: Session = Depends(get_db), svc: TecnicoService = Depends(get_tecnico_service), current_user=Depends(get_current_user)):
    return svc.get_tecnicos(db, current_user)

@tecnico_controller.get("/{tecnico_id}", response_model=TecnicoResponse, dependencies=[Depends(require_permissions(["ver_tecnico"]))])
def get_tecnico(tecnico_id: int, db: Session = Depends(get_db), svc: TecnicoService = Depends(get_tecnico_service), current_user=Depends(get_current_user)):
    try:
        return svc.get_tecnico(db, tecnico_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@tecnico_controller.post("/", response_model=TecnicoResponse, dependencies=[Depends(require_permissions(["crear_tecnico"]))])
def create_tecnico(data: TecnicoCreate, db: Session = Depends(get_db), svc: TecnicoService = Depends(get_tecnico_service), current_user=Depends(get_current_user)):
    try:
        return svc.create_tecnico(db, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@tecnico_controller.patch("/{tecnico_id}", response_model=TecnicoResponse, dependencies=[Depends(require_permissions(["editar_tecnico"]))])
def update_tecnico(tecnico_id: int, data: TecnicoUpdate, db: Session = Depends(get_db), svc: TecnicoService = Depends(get_tecnico_service), current_user=Depends(get_current_user)):
    try:
        return svc.update_tecnico(db, tecnico_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@tecnico_controller.delete("/{tecnico_id}", dependencies=[Depends(require_permissions(["inactivar_tecnico"]))])
def inactivar_tecnico(tecnico_id: int, db: Session = Depends(get_db), svc: TecnicoService = Depends(get_tecnico_service), current_user=Depends(get_current_user)):
    try:
        svc.inactivar_tecnico(db, tecnico_id, current_user)
        return {"message": "Técnico inactivado correctamente."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
