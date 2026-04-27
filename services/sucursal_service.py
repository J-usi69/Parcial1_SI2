from sqlalchemy.orm import Session
from schemas.sucursal import SucursalCreate, SucursalUpdate
from repositories.sucursal_repository import SucursalRepository

class SucursalService:
    def __init__(self, repository: SucursalRepository):
        self.repository = repository

    def get_sucursales(self, db: Session, current_user):
        from models.sucursal import Sucursal
        if current_user.is_staff:
            return self.repository.get_all(db)
        elif current_user.empresa_id:
            return db.query(Sucursal).filter(Sucursal.empresa_id == current_user.empresa_id).all()
        return []

    def get_sucursal(self, db: Session, sucursal_id: int, current_user):
        sucursal = self.repository.get_by_id(db, sucursal_id)
        if not sucursal:
            raise ValueError(f"La Sucursal {sucursal_id} no existe.")
        self._validate_scope(current_user, sucursal.empresa_id)
        return sucursal

    def get_by_empresa(self, db: Session, empresa_id: int, current_user):
        self._validate_scope(current_user, empresa_id)
        return self.repository.get_by_empresa(db, empresa_id)
        
    def _validate_scope(self, current_user, empresa_id):
        if not current_user.is_staff and current_user.empresa_id != empresa_id:
            raise PermissionError("Violación de Ámbito: Acceso denegado a esta sucursal.")

    def create_sucursal(self, db: Session, data: SucursalCreate, current_user):
        self._validate_scope(current_user, data.empresa_id)
        from models.usuario import Usuario
        from models.suscripcion import Suscripcion
        from models.sucursal import Sucursal
        
        # Obtener el dueño de la empresa para ver su suscripción
        owner = db.query(Usuario).filter(Usuario.empresa_id == data.empresa_id, Usuario.is_owner == True).first()
        if not owner:
            raise ValueError("No se puede crear una sucursal para una empresa sin Administrador Principal asignado.")
            
        suscripcion = db.query(Suscripcion).filter(Suscripcion.id == owner.suscripcion_id).first()
        if suscripcion:
            current_sucursales = db.query(Sucursal).filter(Sucursal.empresa_id == data.empresa_id, Sucursal.status == 'activo').count()
            if current_sucursales >= suscripcion.max_sucursales:
                raise ValueError(f"Límite de sucursales alcanzado ({suscripcion.max_sucursales}) para la suscripción operativa del taller.")
                
        return self.repository.create(db, data)

    def update_sucursal(self, db: Session, sucursal_id: int, data: SucursalUpdate, current_user):
        sucursal = self.repository.get_by_id(db, sucursal_id)
        if not sucursal:
            raise ValueError("Sucursal no encontrada")
        self._validate_scope(current_user, sucursal.empresa_id)
            
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, sucursal_id, clean_update)

    def soft_delete_sucursal(self, db: Session, sucursal_id: int, current_user):
        sucursal = self.repository.get_by_id(db, sucursal_id)
        if not sucursal:
            raise ValueError("Sucursal no encontrada")
        self._validate_scope(current_user, sucursal.empresa_id)
        return self.repository.logical_delete(db, sucursal_id)
