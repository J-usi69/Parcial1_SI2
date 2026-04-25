from sqlalchemy.orm import Session
from schemas.rol import RolCreate, RolUpdate
from repositories.rol_repository import RolRepository

class RolService:
    def __init__(self, repository: RolRepository):
        self.repository = repository

    def get_roles(self, db: Session):
        return self.repository.get_all(db)

    def get_rol(self, db: Session, rol_id: int):
        rol = self.repository.get_by_id(db, rol_id)
        if not rol:
            raise ValueError("Rol especificado no hallado en sistema.")
        return rol

    def create_rol(self, db: Session, data: RolCreate):
        existing = self.repository.get_by_nombre(db, data.nombre)
        if existing:
            raise ValueError("El nombre propuesto se encuentra actualmente en uso por otro rol.")
        return self.repository.create(db, data)

    def update_rol(self, db: Session, rol_id: int, data: RolUpdate):
        rol = self.repository.get_by_id(db, rol_id)
        if not rol:
            raise ValueError("Rol Inexistente")
            
        if data.nombre and data.nombre != rol.nombre:
            if self.repository.get_by_nombre(db, data.nombre):
                raise ValueError("Cambio declinado. El nuevo nombre colisiona con otra entidad de permisos vigente.")
                
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, rol_id, clean_update)

    def delete_rol(self, db: Session, rol_id: int):
        rol = self.repository.get_by_id(db, rol_id)
        if not rol:
            raise ValueError("Inexistente.")
        # La DB rechazará si tiene cascada restringida o dependencias.
        return self.repository.delete(db, rol_id)
