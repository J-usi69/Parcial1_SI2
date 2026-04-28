from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from schemas.archivo import ArchivoCreate, ArchivoResponse, ArchivoUpdate
from services.archivo_service import ArchivoService
from repositories.archivo_repository import ArchivoRepository
from services.auth_service import get_current_user, require_permissions

def get_archivo_service():
    return ArchivoService(ArchivoRepository())

router = APIRouter(prefix="/archivos", tags=["Archivos"])

@router.get("/entidad/{entidad_tipo}/{entidad_id}", response_model=List[ArchivoResponse])
def listar_archivos(
    entidad_tipo: str,
    entidad_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_archivo"])),
    service: ArchivoService = Depends(get_archivo_service)
):
    try:
        return service.get_por_entidad(db, entidad_tipo, entidad_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/{archivo_id}", response_model=ArchivoResponse)
def obtener_archivo(
    archivo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["ver_archivo"])),
    service: ArchivoService = Depends(get_archivo_service)
):
    try:
        return service.get_archivo(db, archivo_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=ArchivoResponse)
def subir_archivo(
    data: ArchivoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["crear_archivo"])),
    service: ArchivoService = Depends(get_archivo_service)
):
    try:
        return service.create_archivo(db, data, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{archivo_id}")
def inactivar_archivo(
    archivo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permissions(["inactivar_archivo"])),
    service: ArchivoService = Depends(get_archivo_service)
):
    try:
        service.inactivar_archivo(db, archivo_id, current_user)
        return {"mensaje": "Archivo inactivado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
