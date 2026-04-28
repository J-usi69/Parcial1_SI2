from sqlalchemy.orm import Session
from models.metodo_pago import MetodoPago
from schemas.metodo_pago import MetodoPagoCreate

class MetodoPagoRepository:
    def get_by_id(self, db: Session, metodo_id: int):
        return db.query(MetodoPago).filter(MetodoPago.id == metodo_id).first()

    def get_by_propietario(self, db: Session, propietario_tipo: str, propietario_id: int):
        return db.query(MetodoPago).filter(
            MetodoPago.propietario_tipo == propietario_tipo,
            MetodoPago.propietario_id == propietario_id,
            MetodoPago.status == "activo"
        ).all()

    def create(self, db: Session, data: MetodoPagoCreate) -> MetodoPago:
        db_obj = MetodoPago(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, metodo_id: int, data: dict):
        db.query(MetodoPago).filter(MetodoPago.id == metodo_id).update(data)
        db.commit()
        return self.get_by_id(db, metodo_id)
