from sqlalchemy.orm import Session
from models.rol import Rol
from schemas.rol import RolCreate

class RolRepository:
    def get_by_id(self, db: Session, rol_id: int):
        return db.query(Rol).filter(Rol.id == rol_id).first()
        
    def get_by_nombre(self, db: Session, nombre: str):
        return db.query(Rol).filter(Rol.nombre == nombre).first()

    def get_all(self, db: Session):
        return db.query(Rol).all()

    def create(self, db: Session, data: RolCreate):
        db_obj = Rol(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, rol_id: int, data: dict):
        obj = self.get_by_id(db, rol_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def delete(self, db: Session, rol_id: int):
        obj = self.get_by_id(db, rol_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
