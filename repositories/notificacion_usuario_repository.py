from sqlalchemy.orm import Session
from models.notificacion_usuario import NotificacionUsuario
from schemas.notificacion_usuario import NotificacionUsuarioCreate

class NotificacionUsuarioRepository:
    def get_by_user_and_notif(self, db: Session, usuario_id: int, notificacion_id: int):
        return db.query(NotificacionUsuario).filter(
            NotificacionUsuario.usuario_id == usuario_id,
            NotificacionUsuario.notificacion_id == notificacion_id
        ).first()

    def update_leido(self, db: Session, usuario_id: int, notificacion_id: int):
        obj = self.get_by_user_and_notif(db, usuario_id, notificacion_id)
        if obj:
            obj.leido = True
            db.commit()
            db.refresh(obj)
        return obj

    def get_by_usuario(self, db: Session, usuario_id: int):
        return db.query(NotificacionUsuario).filter(NotificacionUsuario.usuario_id == usuario_id).all()

    def create(self, db: Session, data: NotificacionUsuarioCreate):
        db_obj = NotificacionUsuario(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
