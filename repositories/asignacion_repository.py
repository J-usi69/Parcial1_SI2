from sqlalchemy.orm import Session
from models.asignacion import Asignacion
from schemas.asignacion import AsignacionCreate

class AsignacionRepository:
    def get_by_id(self, db: Session, asignacion_id: int):
        return db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()

    def get_by_solicitud(self, db: Session, solicitud_id: int):
        return db.query(Asignacion).filter(Asignacion.solicitud_id == solicitud_id).all()

    def get_by_tecnico(self, db: Session, tecnico_id: int):
        return db.query(Asignacion).filter(Asignacion.tecnico_id == tecnico_id).all()

    def create(self, db: Session, data: AsignacionCreate):
        db_obj = Asignacion(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, asignacion_id: int, data: dict):
        obj = self.get_by_id(db, asignacion_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj
