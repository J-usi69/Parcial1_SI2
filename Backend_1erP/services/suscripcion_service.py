from sqlalchemy.orm import Session
from schemas.suscripcion import SuscripcionCreate, SuscripcionUpdate
from repositories.suscripcion_repository import SuscripcionRepository

class SuscripcionService:
    def __init__(self, repository: SuscripcionRepository):
        self.repository = repository

    def get_suscripciones(self, db: Session):
        return self.repository.get_all(db)

    def get_suscripcion(self, db: Session, suscripcion_id: int):
        suscripcion = self.repository.get_by_id(db, suscripcion_id)
        if not suscripcion:
            raise ValueError(f"Suscripción {suscripcion_id} no encontrada.")
        return suscripcion

    def create_suscripcion(self, db: Session, data: SuscripcionCreate):
        existing = self.repository.get_by_titulo(db, data.titulo)
        if existing:
            raise ValueError(f"Ya hay un plan con el título {data.titulo}")
        return self.repository.create(db, data)

    def update_suscripcion(self, db: Session, suscripcion_id: int, data: SuscripcionUpdate):
        suscripcion = self.repository.get_by_id(db, suscripcion_id)
        if not suscripcion:
            raise ValueError("Suscripción inexistente.")
            
        if data.titulo and data.titulo != suscripcion.titulo:
            if self.repository.get_by_titulo(db, data.titulo):
                raise ValueError("El título de la suscripción propuesto ya se encuentra colisionado con uno vigente.")
                
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, suscripcion_id, clean_update)

    def desactivar_suscripcion(self, db: Session, suscripcion_id: int):
        suscripcion = self.repository.get_by_id(db, suscripcion_id)
        if not suscripcion:
            raise ValueError("Suscripción irreconocida en base de datos.")
        return self.repository.logical_delete(db, suscripcion_id)
