from sqlalchemy.orm import Session
from models.rol_permiso import RolPermiso
from schemas.rol_permiso import RolPermisoCreate

class RolPermisoRepository:
    def get_by_rol_and_permiso(self, db: Session, rol_id: int, permiso_id: int):
        return db.query(RolPermiso).filter(
            RolPermiso.rol_id == rol_id,
            RolPermiso.permiso_id == permiso_id
        ).first()

    def get_permisos_by_rol(self, db: Session, rol_id: int):
        return db.query(RolPermiso).filter(RolPermiso.rol_id == rol_id).all()

    def update_vigencia(self, db: Session, rol_id: int, permiso_id: int, vigente: bool):
        obj = self.get_by_rol_and_permiso(db, rol_id, permiso_id)
        if obj:
            obj.vigente = vigente
            db.commit()
            db.refresh(obj)
        return obj

    def create(self, db: Session, data: RolPermisoCreate):
        db_obj = RolPermiso(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
