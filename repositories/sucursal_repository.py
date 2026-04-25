from sqlalchemy.orm import Session
from models.sucursal import Sucursal
from schemas.sucursal import SucursalCreate

class SucursalRepository:
    def get_by_id(self, db: Session, sucursal_id: int):
        return db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()
        
    def get_all(self, db: Session):
        return db.query(Sucursal).all()
        
    def get_by_empresa(self, db: Session, empresa_id: int):
        return db.query(Sucursal).filter(Sucursal.empresa_id == empresa_id).all()
        
    def create(self, db: Session, data: SucursalCreate):
        db_obj = Sucursal(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, sucursal_id: int, data: dict):
        obj = self.get_by_id(db, sucursal_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def logical_delete(self, db: Session, sucursal_id: int):
        obj = self.get_by_id(db, sucursal_id)
        if obj:
            obj.status = "inactivo"
            db.commit()
            db.refresh(obj)
        return obj
