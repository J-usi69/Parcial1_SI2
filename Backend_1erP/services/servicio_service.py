from sqlalchemy.orm import Session
from schemas.servicio import ServicioCreate, ServicioUpdate
from repositories.servicio_repository import ServicioRepository

class ServicioService:
    def __init__(self, repository: ServicioRepository):
        self.repository = repository

    def get_servicios(self, db: Session, current_user):
        if current_user.is_staff:
            return self.repository.get_all(db)
        elif current_user.empresa_id:
            return self.repository.get_by_empresa(db, current_user.empresa_id)
        return []

    def get_servicio(self, db: Session, servicio_id: int, current_user):
        servicio = self.repository.get_by_id(db, servicio_id)
        if not servicio:
            raise ValueError(f"Servicio {servicio_id} no encontrado.")
        self._validate_scope(current_user, servicio.empresa_id)
        return servicio

    def create_servicio(self, db: Session, data: ServicioCreate, current_user):
        self._validate_scope(current_user, data.empresa_id)
        return self.repository.create(db, data)

    def update_servicio(self, db: Session, servicio_id: int, data: ServicioUpdate, current_user):
        servicio = self.repository.get_by_id(db, servicio_id)
        if not servicio:
            raise ValueError("Servicio no encontrado.")
        self._validate_scope(current_user, servicio.empresa_id)
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, servicio_id, clean_update)

    def inactivar_servicio(self, db: Session, servicio_id: int, current_user):
        servicio = self.repository.get_by_id(db, servicio_id)
        if not servicio:
            raise ValueError("Servicio no encontrado.")
        self._validate_scope(current_user, servicio.empresa_id)
        return self.repository.logical_delete(db, servicio_id)

    def _validate_scope(self, current_user, empresa_id: int):
        if not current_user.is_staff and current_user.empresa_id != empresa_id:
            raise PermissionError("Violación de Ámbito: Acceso denegado a este servicio.")
