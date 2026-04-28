from sqlalchemy.orm import Session
from schemas.vehiculo import VehiculoCreate, VehiculoUpdate
from repositories.vehiculo_repository import VehiculoRepository

class VehiculoService:
    def __init__(self, repository: VehiculoRepository):
        self.repository = repository

    def get_vehiculos(self, db: Session, current_user):
        if current_user.is_staff:
            return self.repository.get_all(db)
        return self.repository.get_by_usuario(db, current_user.id)

    def get_vehiculo(self, db: Session, vehiculo_id: int, current_user):
        vehiculo = self.repository.get_by_id(db, vehiculo_id)
        if not vehiculo:
            raise ValueError(f"Vehículo {vehiculo_id} no encontrado.")
        self._validate_scope(current_user, vehiculo.usuario_id)
        return vehiculo

    def create_vehiculo(self, db: Session, data: VehiculoCreate, current_user):
        # Solo el propio cliente o un staff puede registrar vehículos
        if not current_user.is_staff and data.usuario_id != current_user.id:
            raise PermissionError("Violación de Ámbito: Solo puedes registrar vehículos a tu propio usuario.")
        return self.repository.create(db, data)

    def update_vehiculo(self, db: Session, vehiculo_id: int, data: VehiculoUpdate, current_user):
        vehiculo = self.repository.get_by_id(db, vehiculo_id)
        if not vehiculo:
            raise ValueError("Vehículo no encontrado.")
        self._validate_scope(current_user, vehiculo.usuario_id)
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, vehiculo_id, clean_update)

    def inactivar_vehiculo(self, db: Session, vehiculo_id: int, current_user):
        vehiculo = self.repository.get_by_id(db, vehiculo_id)
        if not vehiculo:
            raise ValueError("Vehículo no encontrado.")
        self._validate_scope(current_user, vehiculo.usuario_id)
        return self.repository.logical_delete(db, vehiculo_id)

    def _validate_scope(self, current_user, usuario_id: int):
        if not current_user.is_staff and current_user.id != usuario_id:
            raise PermissionError("Violación de Ámbito: No tienes permiso para acceder a este vehículo.")
