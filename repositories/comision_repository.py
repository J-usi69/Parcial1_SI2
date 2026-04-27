from sqlalchemy.orm import Session
from models.comision import Comision
from schemas.comision import ComisionCreate

class ComisionRepository:
    def get_by_id(self, db: Session, comision_id: int):
        return db.query(Comision).filter(Comision.id == comision_id).first()

    def get_by_solicitud(self, db: Session, solicitud_id: int):
        return db.query(Comision).filter(Comision.solicitud_id == solicitud_id).first()

    def get_by_tecnico(self, db: Session, tecnico_id: int):
        return db.query(Comision).filter(Comision.tecnico_id == tecnico_id).all()

    def create(self, db: Session, data: ComisionCreate) -> Comision:
        db_obj = Comision(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, comision_id: int, data: dict):
        db.query(Comision).filter(Comision.id == comision_id).update(data)
        db.commit()
        return self.get_by_id(db, comision_id)
