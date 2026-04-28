from sqlalchemy.orm import Session
from schemas.servicio_sucursal import ServicioSucursalCreate, ServicioSucursalUpdate
from repositories.servicio_sucursal_repository import ServicioSucursalRepository

class ServicioSucursalService:
    def __init__(self, repository: ServicioSucursalRepository):
        self.repository = repository

    def get_por_sucursal(self, db: Session, sucursal_id: int, current_user):
        from models.sucursal import Sucursal
        sucursal = db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()
        if not sucursal:
            raise ValueError("Sucursal no encontrada.")
        self._validate_scope(current_user, sucursal.empresa_id)
        return self.repository.get_by_sucursal(db, sucursal_id)

    def get_servicio_sucursal(self, db: Session, ss_id: int, current_user):
        ss = self.repository.get_by_id(db, ss_id)
        if not ss:
            raise ValueError(f"ServicioSucursal {ss_id} no encontrado.")
        self._validate_scope_by_ss(db, current_user, ss)
        return ss

    def asignar(self, db: Session, data: ServicioSucursalCreate, current_user):
        from models.sucursal import Sucursal
        sucursal = db.query(Sucursal).filter(Sucursal.id == data.sucursal_id).first()
        if not sucursal:
            raise ValueError("Sucursal no encontrada.")
        self._validate_scope(current_user, sucursal.empresa_id)
        # Evitar duplicados: verificar si ya existe la combinación
        existing = self.repository.get_disponible(db, data.servicio_id, data.sucursal_id)
        if existing:
            raise ValueError("El servicio ya está asignado a esta sucursal.")
        return self.repository.create(db, data)

    def editar(self, db: Session, ss_id: int, data: ServicioSucursalUpdate, current_user):
        ss = self.repository.get_by_id(db, ss_id)
        if not ss:
            raise ValueError("ServicioSucursal no encontrado.")
        self._validate_scope_by_ss(db, current_user, ss)
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, ss_id, clean_update)

    def inactivar(self, db: Session, ss_id: int, current_user):
        ss = self.repository.get_by_id(db, ss_id)
        if not ss:
            raise ValueError("ServicioSucursal no encontrado.")
        self._validate_scope_by_ss(db, current_user, ss)
        return self.repository.logical_delete(db, ss_id)

    def _validate_scope(self, current_user, empresa_id: int):
        if not current_user.is_staff and current_user.empresa_id != empresa_id:
            raise PermissionError("Violación de Ámbito: Acceso denegado a este servicio de sucursal.")

    def _validate_scope_by_ss(self, db: Session, current_user, ss):
        from models.sucursal import Sucursal
        sucursal = db.query(Sucursal).filter(Sucursal.id == ss.sucursal_id).first()
        if sucursal:
            self._validate_scope(current_user, sucursal.empresa_id)
