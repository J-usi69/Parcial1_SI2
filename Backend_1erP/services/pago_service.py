from sqlalchemy.orm import Session
from datetime import datetime, timezone
from schemas.pago import PagoCreate, PagoUpdate, PagoVerify
from repositories.pago_repository import PagoRepository
from models.solicitud import Solicitud
from models.sucursal import Sucursal
from models.enums import EstadoPago

class PagoService:
    def __init__(self, repository: PagoRepository):
        self.repository = repository

    def _validate_scope(self, db: Session, current_user, pago):
        if current_user.is_staff:
            return
        if current_user.type == "cliente" and pago.cliente_id != current_user.id:
            raise PermissionError("No puedes ver pagos de otros clientes.")
        if current_user.type == "empresa" and current_user.empresa_id:
            sol = db.query(Solicitud).filter(Solicitud.id == pago.solicitud_id).first()
            suc = db.query(Sucursal).filter(Sucursal.id == sol.sucursal_id).first()
            if not suc or suc.empresa_id != current_user.empresa_id:
                raise PermissionError("No tienes acceso a los pagos de esta solicitud.")

    def get_pago(self, db: Session, pago_id: int, current_user):
        pago = self.repository.get_by_id(db, pago_id)
        if not pago:
            raise ValueError("Pago no encontrado.")
        self._validate_scope(db, current_user, pago)
        return pago

    def get_por_solicitud(self, db: Session, solicitud_id: int, current_user):
        pago = self.repository.get_by_solicitud(db, solicitud_id)
        if pago:
            self._validate_scope(db, current_user, pago)
        return pago

    def get_pagos_cliente(self, db: Session, cliente_id: int, current_user):
        if not current_user.is_staff and current_user.id != cliente_id:
            raise PermissionError("No puedes ver pagos de otros clientes.")
        return self.repository.get_by_cliente(db, cliente_id)

    def get_pagos_empresa(self, db: Session, empresa_id: int, current_user):
        if not current_user.is_staff and current_user.empresa_id != empresa_id:
            raise PermissionError("No puedes ver pagos de otras empresas.")
        # Filtrar pagos cuyas solicitudes pertenecen a la empresa
        from models.pago import Pago
        return db.query(Pago).join(Solicitud).join(Sucursal).filter(Sucursal.empresa_id == empresa_id).all()

    def create_pago(self, db: Session, data: PagoCreate, current_user):
        sol = db.query(Solicitud).filter(Solicitud.id == data.solicitud_id).first()
        if not sol:
            raise ValueError("Solicitud no encontrada.")
            
        # IMPONER cliente_id desde el token si es un cliente
        cliente_id_final = current_user.id if current_user.type == "cliente" else sol.cliente_id
        
        if current_user.type == "cliente" and sol.cliente_id != current_user.id:
            raise PermissionError("No puedes pagar una solicitud que no es tuya.")
            
        if sol.estado in ["rechazada", "cancelada"]:
            raise ValueError("No se puede registrar pago para una solicitud rechazada o cancelada.")
            
        existente = self.repository.get_by_solicitud(db, data.solicitud_id)
        if existente:
            raise ValueError("Ya existe un pago para esta solicitud.")
            
        # Inyectar cliente_id derivado
        db_obj = self.repository.create(db, data)
        db_obj.cliente_id = cliente_id_final
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_estado(self, db: Session, pago_id: int, data: PagoUpdate, current_user):
        pago = self.get_pago(db, pago_id, current_user)
        clean_data = data.model_dump(exclude_unset=True)
        if data.estado_pago == EstadoPago.pagado and pago.estado_pago == EstadoPago.pendiente:
            clean_data["fecha_pago"] = datetime.now(timezone.utc)
        return self.repository.update(db, pago_id, clean_data)

    def verificar_pago(self, db: Session, pago_id: int, data: PagoVerify, current_user):
        pago = self.get_pago(db, pago_id, current_user)
        if current_user.type == "cliente":
            raise PermissionError("Los clientes no pueden verificar pagos.")
            
        update_data = {
            "estado_pago": EstadoPago.verificado,
            "verificado_por_usuario_id": current_user.id,
            "fecha_verificacion": datetime.now(timezone.utc)
        }
        if data.observacion:
            update_data["observacion"] = data.observacion
            
        return self.repository.update(db, pago_id, update_data)
