from sqlalchemy.orm import Session
from models.archivo import Archivo
from schemas.archivo import ArchivoCreate, ArchivoUpdate

class ArchivoRepository:
    def get_by_id(self, db: Session, archivo_id: int):
        return db.query(Archivo).filter(Archivo.id == archivo_id).first()

    def get_by_entidad(self, db: Session, entidad_tipo: str, entidad_id: int):
        return db.query(Archivo).filter(Archivo.entidad_tipo == entidad_tipo, Archivo.entidad_id == entidad_id, Archivo.status == "activo").all()

    def create(self, db: Session, data: ArchivoCreate, subido_por_id: int, nombre_interno: str, ruta: str) -> Archivo:
        db_obj = Archivo(
            **data.model_dump(),
            subido_por_id=subido_por_id,
            nombre_interno=nombre_interno,
            ruta=ruta
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, archivo_id: int, data: dict):
        db.query(Archivo).filter(Archivo.id == archivo_id).update(data)
        db.commit()
        return self.get_by_id(db, archivo_id)
