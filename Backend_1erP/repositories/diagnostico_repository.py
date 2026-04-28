from sqlalchemy.orm import Session
from models.diagnostico import Diagnostico
from schemas.diagnostico import DiagnosticoCreate

class DiagnosticoRepository:
    def get_by_id(self, db: Session, diagnostico_id: int):
        return db.query(Diagnostico).filter(Diagnostico.id == diagnostico_id).first()

    def get_by_asignacion(self, db: Session, asignacion_id: int):
        return db.query(Diagnostico).filter(Diagnostico.asignacion_id == asignacion_id).first()

    def create(self, db: Session, data: DiagnosticoCreate):
        db_obj = Diagnostico(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, diagnostico_id: int, data: dict):
        obj = self.get_by_id(db, diagnostico_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj
