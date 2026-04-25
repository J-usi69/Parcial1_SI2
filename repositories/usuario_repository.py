from sqlalchemy.orm import Session
from models.usuario import Usuario

class UsuarioRepository:
    def get_by_id(self, db: Session, user_id: int):
        return db.query(Usuario).filter(Usuario.id == user_id).first()
        
    def get_by_correo(self, db: Session, correo: str):
        return db.query(Usuario).filter(Usuario.correo == correo).first()
        
    def get_all(self, db: Session):
        return db.query(Usuario).all()
        
    def create(self, db: Session, data: dict):
        db_obj = Usuario(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    def update_last_con(self, db: Session, user_id: int, date_val):
        user = self.get_by_id(db, user_id)
        if user:
            user.last_con = date_val
            db.commit()
            db.refresh(user)
        return user

    def update_perfil(self, db: Session, user_id: int, data: dict):
        user = self.get_by_id(db, user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user

    def set_inactive(self, db: Session, user_id: int):
        user = self.get_by_id(db, user_id)
        if user:
            user.is_active = False
            db.commit()
            db.refresh(user)
        return user
