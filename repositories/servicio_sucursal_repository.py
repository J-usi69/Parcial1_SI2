from sqlalchemy.orm import Session
from models.servicio_sucursal import ServicioSucursal
from schemas.servicio_sucursal import ServicioSucursalCreate

class ServicioSucursalRepository:
    def get_by_id(self, db: Session, ss_id: int):
        return db.query(ServicioSucursal).filter(ServicioSucursal.id == ss_id).first()

    def get_all(self, db: Session):
        return db.query(ServicioSucursal).all()

    def get_by_sucursal(self, db: Session, sucursal_id: int):
        return db.query(ServicioSucursal).filter(ServicioSucursal.sucursal_id == sucursal_id).all()

    def get_by_servicio(self, db: Session, servicio_id: int):
        return db.query(ServicioSucursal).filter(ServicioSucursal.servicio_id == servicio_id).all()

    def get_disponible(self, db: Session, servicio_id: int, sucursal_id: int):
        return db.query(ServicioSucursal).filter(
            ServicioSucursal.servicio_id == servicio_id,
            ServicioSucursal.sucursal_id == sucursal_id,
            ServicioSucursal.disponible == True
        ).first()

    def create(self, db: Session, data: ServicioSucursalCreate):
        db_obj = ServicioSucursal(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, ss_id: int, data: dict):
        obj = self.get_by_id(db, ss_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def logical_delete(self, db: Session, ss_id: int):
        obj = self.get_by_id(db, ss_id)
        if obj:
            obj.disponible = False
            db.commit()
            db.refresh(obj)
        return obj
