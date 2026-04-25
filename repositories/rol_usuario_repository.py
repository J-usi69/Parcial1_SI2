from sqlalchemy.orm import Session
from models.rol_usuario import RolUsuario
from schemas.rol_usuario import RolUsuarioCreate

class RolUsuarioRepository:
    def get_by_user_and_rol(self, db: Session, rol_id: int, usuario_id: int):
        return db.query(RolUsuario).filter(
            RolUsuario.rol_id == rol_id,
            RolUsuario.usuario_id == usuario_id
        ).first()

    def get_roles_by_user(self, db: Session, usuario_id: int):
        return db.query(RolUsuario).filter(RolUsuario.usuario_id == usuario_id).all()

    def delete(self, db: Session, rol_id: int, usuario_id: int):
        obj = self.get_by_user_and_rol(db, rol_id, usuario_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def create(self, db: Session, data: RolUsuarioCreate):
        db_obj = RolUsuario(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
