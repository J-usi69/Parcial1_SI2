from sqlalchemy.orm import Session
from schemas.metodo_pago import MetodoPagoCreate, MetodoPagoUpdate
from repositories.metodo_pago_repository import MetodoPagoRepository
from models.sucursal import Sucursal

class MetodoPagoService:
    def __init__(self, repository: MetodoPagoRepository):
        self.repository = repository

    def _validate_scope(self, db: Session, current_user, propietario_tipo: str, propietario_id: int):
        if current_user.is_staff:
            return
        if propietario_tipo == "cliente":
            if current_user.id != propietario_id:
                raise PermissionError("No puedes gestionar métodos de pago de otros clientes.")
        elif propietario_tipo == "sucursal":
            if not current_user.empresa_id:
                raise PermissionError("Usuario no pertenece a ninguna empresa.")
            suc = db.query(Sucursal).filter(Sucursal.id == propietario_id).first()
            if not suc or suc.empresa_id != current_user.empresa_id:
                raise PermissionError("No tienes acceso a los métodos de pago de esta sucursal.")
        else:
            raise ValueError("Tipo de propietario no válido.")

    def get_metodo(self, db: Session, metodo_id: int, current_user):
        metodo = self.repository.get_by_id(db, metodo_id)
        if not metodo:
            raise ValueError("Método de pago no encontrado.")
        self._validate_scope(db, current_user, metodo.propietario_tipo, metodo.propietario_id)
        return metodo

    def get_por_propietario(self, db: Session, propietario_tipo: str, propietario_id: int, current_user):
        self._validate_scope(db, current_user, propietario_tipo, propietario_id)
        return self.repository.get_by_propietario(db, propietario_tipo, propietario_id)

    def create_metodo(self, db: Session, data: MetodoPagoCreate, current_user):
        self._validate_scope(db, current_user, data.propietario_tipo, data.propietario_id)
        return self.repository.create(db, data)

    def update_metodo(self, db: Session, metodo_id: int, data: MetodoPagoUpdate, current_user):
        metodo = self.get_metodo(db, metodo_id, current_user)
        clean_data = data.model_dump(exclude_unset=True)
        return self.repository.update(db, metodo_id, clean_data)

    def inactivar_metodo(self, db: Session, metodo_id: int, current_user):
        metodo = self.get_metodo(db, metodo_id, current_user)
        return self.repository.update(db, metodo_id, {"status": "inactivo"})
