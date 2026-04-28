from sqlalchemy.orm import Session
from models.vehiculo import Vehiculo
from schemas.vehiculo import VehiculoCreate

class VehiculoRepository:
    def get_by_id(self, db: Session, vehiculo_id: int):
        return db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()

    def get_all(self, db: Session):
        return db.query(Vehiculo).all()

    def get_by_usuario(self, db: Session, usuario_id: int):
        return db.query(Vehiculo).filter(Vehiculo.usuario_id == usuario_id).all()

    def create(self, db: Session, data: VehiculoCreate):
        db_obj = Vehiculo(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, vehiculo_id: int, data: dict):
        obj = self.get_by_id(db, vehiculo_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def logical_delete(self, db: Session, vehiculo_id: int):
        obj = self.get_by_id(db, vehiculo_id)
        if obj:
            obj.status = "inactivo"
            db.commit()
            db.refresh(obj)
        return obj
