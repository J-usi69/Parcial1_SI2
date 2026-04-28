from sqlalchemy.orm import Session
from models.pago import Pago
from schemas.pago import PagoCreate

class PagoRepository:
    def get_by_id(self, db: Session, pago_id: int):
        return db.query(Pago).filter(Pago.id == pago_id).first()

    def get_by_solicitud(self, db: Session, solicitud_id: int):
        return db.query(Pago).filter(Pago.solicitud_id == solicitud_id).first()

    def get_by_cliente(self, db: Session, cliente_id: int):
        return db.query(Pago).filter(Pago.cliente_id == cliente_id).all()

    def create(self, db: Session, data: PagoCreate) -> Pago:
        db_obj = Pago(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, pago_id: int, data: dict):
        db.query(Pago).filter(Pago.id == pago_id).update(data)
        db.commit()
        return self.get_by_id(db, pago_id)
