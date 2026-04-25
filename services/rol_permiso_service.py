from sqlalchemy.orm import Session
from schemas.rol_permiso import RolPermisoCreate
from repositories.rol_permiso_repository import RolPermisoRepository

class RolPermisoService:
    def __init__(self, repository: RolPermisoRepository):
        self.repository = repository

    def asignar_permiso(self, db: Session, data: RolPermisoCreate):
        existing = self.repository.get_by_rol_and_permiso(db, data.rol_id, data.permiso_id)
        if existing:
            raise ValueError("El permiso ya está asignado a este rol.")
        return self.repository.create(db, data)

    def get_permisos_by_rol(self, db: Session, rol_id: int):
        return self.repository.get_permisos_by_rol(db, rol_id)

    def update_vigencia(self, db: Session, rol_id: int, permiso_id: int, vigente: bool):
        existing = self.repository.get_by_rol_and_permiso(db, rol_id, permiso_id)
        if not existing:
            raise ValueError("Asignación originaria inexistente.")
        return self.repository.update_vigencia(db, rol_id, permiso_id, vigente)
