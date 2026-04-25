from sqlalchemy.orm import Session
from models.permiso import Permiso
from schemas.permiso import PermisoCreate

class PermisoRepository:
    def get_by_id(self, db: Session, permiso_id: int):
        return db.query(Permiso).filter(Permiso.id == permiso_id).first()
        
    def get_by_nombre(self, db: Session, nombre: str):
        return db.query(Permiso).filter(Permiso.nombre == nombre).first()

    def get_all(self, db: Session):
        return db.query(Permiso).all()

    def create(self, db: Session, data: PermisoCreate):
        db_obj = Permiso(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, permiso_id: int, data: dict):
        obj = self.get_by_id(db, permiso_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def delete(self, db: Session, permiso_id: int):
        obj = self.get_by_id(db, permiso_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
