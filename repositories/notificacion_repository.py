from sqlalchemy.orm import Session
from models.notificacion import Notificacion
from schemas.notificacion import NotificacionCreate

class NotificacionRepository:
    def get_by_id(self, db: Session, notif_id: int):
        return db.query(Notificacion).filter(Notificacion.id == notif_id).first()
        
    def get_all(self, db: Session):
        return db.query(Notificacion).all()
        
    def create(self, db: Session, data: NotificacionCreate):
        db_obj = Notificacion(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
