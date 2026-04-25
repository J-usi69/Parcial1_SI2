from sqlalchemy.orm import Session
from schemas.permiso import PermisoCreate, PermisoUpdate
from repositories.permiso_repository import PermisoRepository

class PermisoService:
    def __init__(self, repository: PermisoRepository):
        self.repository = repository

    def get_permisos(self, db: Session):
        return self.repository.get_all(db)

    def get_permiso(self, db: Session, permiso_id: int):
        permiso = self.repository.get_by_id(db, permiso_id)
        if not permiso:
            raise ValueError("Comando operativo de permiso no hallado.")
        return permiso

    def create_permiso(self, db: Session, data: PermisoCreate):
        existing = self.repository.get_by_nombre(db, data.nombre)
        if existing:
            raise ValueError("Violación: El nombre de permiso propuesto entra en intercepción de colisión con otro vigente.")
        return self.repository.create(db, data)

    def update_permiso(self, db: Session, permiso_id: int, data: PermisoUpdate):
        permiso = self.repository.get_by_id(db, permiso_id)
        if not permiso:
            raise ValueError("No estructurado.")
            
        if data.nombre and data.nombre != permiso.nombre:
            if self.repository.get_by_nombre(db, data.nombre):
                raise ValueError("Cambio inoperativo. El nombre alternativo ya forma parte de otro marco del sistema.")
                
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, permiso_id, clean_update)

    def delete_permiso(self, db: Session, permiso_id: int):
        permiso = self.repository.get_by_id(db, permiso_id)
        if not permiso:
            raise ValueError("Identificador ilusorio.")
        return self.repository.delete(db, permiso_id)
