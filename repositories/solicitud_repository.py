from sqlalchemy.orm import Session
from models.solicitud import Solicitud
from schemas.solicitud import SolicitudCreate

class SolicitudRepository:
    def get_by_id(self, db: Session, solicitud_id: int):
        return db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()

    def get_all(self, db: Session):
        return db.query(Solicitud).all()

    def get_by_cliente(self, db: Session, cliente_id: int):
        return db.query(Solicitud).filter(Solicitud.cliente_id == cliente_id).all()

    def get_by_sucursal(self, db: Session, sucursal_id: int):
        return db.query(Solicitud).filter(Solicitud.sucursal_id == sucursal_id).all()

    def get_by_empresa(self, db: Session, empresa_id: int):
        """Solicitudes de todas las sucursales de una empresa."""
        from models.sucursal import Sucursal
        return (
            db.query(Solicitud)
            .join(Sucursal, Solicitud.sucursal_id == Sucursal.id)
            .filter(Sucursal.empresa_id == empresa_id)
            .all()
        )

    def create(self, db: Session, data: SolicitudCreate):
        db_obj = Solicitud(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, solicitud_id: int, data: dict):
        obj = self.get_by_id(db, solicitud_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj
