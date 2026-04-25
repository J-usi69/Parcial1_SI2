from sqlalchemy.orm import Session
from schemas.sucursal import SucursalCreate, SucursalUpdate
from repositories.sucursal_repository import SucursalRepository

class SucursalService:
    def __init__(self, repository: SucursalRepository):
        self.repository = repository

    def get_sucursales(self, db: Session):
        return self.repository.get_all(db)

    def get_sucursal(self, db: Session, sucursal_id: int):
        sucursal = self.repository.get_by_id(db, sucursal_id)
        if not sucursal:
            raise ValueError(f"La Sucursal {sucursal_id} no existe.")
        return sucursal

    def get_by_empresa(self, db: Session, empresa_id: int):
        return self.repository.get_by_empresa(db, empresa_id)

    def create_sucursal(self, db: Session, data: SucursalCreate):
        return self.repository.create(db, data)

    def update_sucursal(self, db: Session, sucursal_id: int, data: SucursalUpdate):
        sucursal = self.repository.get_by_id(db, sucursal_id)
        if not sucursal:
            raise ValueError("Sucursal no encontrada")
            
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, sucursal_id, clean_update)

    def soft_delete_sucursal(self, db: Session, sucursal_id: int):
        sucursal = self.repository.get_by_id(db, sucursal_id)
        if not sucursal:
            raise ValueError("Sucursal no encontrada")
        return self.repository.logical_delete(db, sucursal_id)
