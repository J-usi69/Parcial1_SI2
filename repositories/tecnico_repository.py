from sqlalchemy.orm import Session
from models.tecnico import Tecnico
from schemas.tecnico import TecnicoCreate

class TecnicoRepository:
    def get_by_id(self, db: Session, tecnico_id: int):
        return db.query(Tecnico).filter(Tecnico.id == tecnico_id).first()

    def get_by_usuario_id(self, db: Session, usuario_id: int):
        return db.query(Tecnico).filter(Tecnico.usuario_id == usuario_id).first()

    def get_all(self, db: Session):
        return db.query(Tecnico).all()

    def get_by_empresa(self, db: Session, empresa_id: int):
        """Obtiene técnicos filtrando por empresa vía join con usuarios."""
        from models.usuario import Usuario
        return (
            db.query(Tecnico)
            .join(Usuario, Tecnico.usuario_id == Usuario.id)
            .filter(Usuario.empresa_id == empresa_id)
            .all()
        )

    def get_activos_por_sucursal(self, db: Session, sucursal_id: int):
        """Técnicos activos (no ocupados) de una sucursal específica."""
        from models.usuario import Usuario
        return (
            db.query(Tecnico)
            .join(Usuario, Tecnico.usuario_id == Usuario.id)
            .filter(
                Usuario.sucursal_id == sucursal_id,
                Tecnico.estado_operativo == "activo"
            )
            .all()
        )

    def create(self, db: Session, data: TecnicoCreate):
        db_obj = Tecnico(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, tecnico_id: int, data: dict):
        obj = self.get_by_id(db, tecnico_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def logical_delete(self, db: Session, tecnico_id: int):
        obj = self.get_by_id(db, tecnico_id)
        if obj:
            obj.estado_operativo = "inactivo"
            db.commit()
            db.refresh(obj)
        return obj
