from sqlalchemy.orm import Session
from models.servicio import Servicio
from schemas.servicio import ServicioCreate

class ServicioRepository:
    def get_by_id(self, db: Session, servicio_id: int):
        return db.query(Servicio).filter(Servicio.id == servicio_id).first()

    def get_all(self, db: Session):
        return db.query(Servicio).all()

    def get_by_empresa(self, db: Session, empresa_id: int):
        return db.query(Servicio).filter(Servicio.empresa_id == empresa_id).all()

    def create(self, db: Session, data: ServicioCreate):
        db_obj = Servicio(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, servicio_id: int, data: dict):
        obj = self.get_by_id(db, servicio_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def logical_delete(self, db: Session, servicio_id: int):
        obj = self.get_by_id(db, servicio_id)
        if obj:
            obj.status = "inactivo"
            db.commit()
            db.refresh(obj)
        return obj
