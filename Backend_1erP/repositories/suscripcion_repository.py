from sqlalchemy.orm import Session
from models.suscripcion import Suscripcion
from schemas.suscripcion import SuscripcionCreate

class SuscripcionRepository:
    def get_by_id(self, db: Session, suscripcion_id: int):
        return db.query(Suscripcion).filter(Suscripcion.id == suscripcion_id).first()
        
    def get_by_titulo(self, db: Session, titulo: str):
        return db.query(Suscripcion).filter(Suscripcion.titulo == titulo).first()
        
    def get_all(self, db: Session):
        return db.query(Suscripcion).all()
        
    def create(self, db: Session, data: SuscripcionCreate):
        db_obj = Suscripcion(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, suscripcion_id: int, data: dict):
        obj = self.get_by_id(db, suscripcion_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def logical_delete(self, db: Session, suscripcion_id: int):
        obj = self.get_by_id(db, suscripcion_id)
        if obj:
            obj.estado = False
            db.commit()
            db.refresh(obj)
        return obj
