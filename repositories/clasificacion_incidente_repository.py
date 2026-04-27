from sqlalchemy.orm import Session
from models.clasificacion_incidente import ClasificacionIncidente
from schemas.clasificacion_incidente import ClasificacionIncidenteCreate

class ClasificacionIncidenteRepository:
    def get_by_id(self, db: Session, clasificacion_id: int):
        return db.query(ClasificacionIncidente).filter(ClasificacionIncidente.id == clasificacion_id).first()

    def get_by_solicitud(self, db: Session, solicitud_id: int):
        return db.query(ClasificacionIncidente).filter(ClasificacionIncidente.solicitud_id == solicitud_id).order_by(ClasificacionIncidente.created_at.desc()).all()

    def get_latest_by_solicitud(self, db: Session, solicitud_id: int):
        return db.query(ClasificacionIncidente).filter(ClasificacionIncidente.solicitud_id == solicitud_id).order_by(ClasificacionIncidente.created_at.desc()).first()

    def create(self, db: Session, data: ClasificacionIncidenteCreate) -> ClasificacionIncidente:
        db_obj = ClasificacionIncidente(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, clasificacion_id: int, data: dict):
        db.query(ClasificacionIncidente).filter(ClasificacionIncidente.id == clasificacion_id).update(data)
        db.commit()
        return self.get_by_id(db, clasificacion_id)
