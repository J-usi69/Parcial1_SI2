from sqlalchemy.orm import Session
from models.empresa import Empresa
from schemas.empresa import EmpresaCreate

class EmpresaRepository:
    def get_by_id(self, db: Session, empresa_id: int):
        return db.query(Empresa).filter(Empresa.id == empresa_id).first()
        
    def get_by_nit(self, db: Session, nit: str):
        return db.query(Empresa).filter(Empresa.nit == nit).first()
        
    def get_all(self, db: Session):
        return db.query(Empresa).all()
        
    def create(self, db: Session, data: EmpresaCreate):
        db_obj = Empresa(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, empresa_id: int, data: dict):
        obj = self.get_by_id(db, empresa_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def logical_delete(self, db: Session, empresa_id: int):
        obj = self.get_by_id(db, empresa_id)
        if obj:
            obj.status = "inactivo"
            db.commit()
            db.refresh(obj)
        return obj
