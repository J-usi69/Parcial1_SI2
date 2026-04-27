from sqlalchemy.orm import Session
from models.recomendacion_sucursal import RecomendacionSucursal
from schemas.recomendacion_sucursal import RecomendacionSucursalCreate

class RecomendacionSucursalRepository:
    def get_by_id(self, db: Session, recomendacion_id: int):
        return db.query(RecomendacionSucursal).filter(RecomendacionSucursal.id == recomendacion_id).first()

    def get_by_solicitud(self, db: Session, solicitud_id: int):
        return db.query(RecomendacionSucursal).filter(RecomendacionSucursal.solicitud_id == solicitud_id).order_by(RecomendacionSucursal.score_recomendacion.desc()).all()

    def create(self, db: Session, data: RecomendacionSucursalCreate) -> RecomendacionSucursal:
        db_obj = RecomendacionSucursal(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, recomendacion_id: int, data: dict):
        db.query(RecomendacionSucursal).filter(RecomendacionSucursal.id == recomendacion_id).update(data)
        db.commit()
        return self.get_by_id(db, recomendacion_id)
