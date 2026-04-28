from sqlalchemy.orm import Session
from datetime import datetime, timezone
from schemas.comision import ComisionCreate, ComisionUpdate
from repositories.comision_repository import ComisionRepository
from models.solicitud import Solicitud
from models.pago import Pago
from models.tecnico import Tecnico
from models.asignacion import Asignacion
from models.enums import EstadoAsignacion, EstadoSolicitud, EstadoPago

class ComisionService:
    def __init__(self, repository: ComisionRepository):
        self.repository = repository

    def _validate_scope(self, db: Session, current_user, comision):
        if current_user.is_staff:
            return
        if current_user.type == "cliente":
            raise PermissionError("Los clientes no tienen acceso a comisiones.")
        
        tecnico = db.query(Tecnico).filter(Tecnico.usuario_id == current_user.id).first()
        if tecnico and comision.tecnico_id == tecnico.id:
            return # El técnico puede ver su propia comisión
            
        # Validación empresa
        sol = db.query(Solicitud).filter(Solicitud.id == comision.solicitud_id).first()
        from models.sucursal import Sucursal
        suc = db.query(Sucursal).filter(Sucursal.id == sol.sucursal_id).first()
        if not suc or suc.empresa_id != current_user.empresa_id:
            raise PermissionError("No tienes acceso a comisiones de otras empresas.")

    def get_comision(self, db: Session, comision_id: int, current_user):
        comision = self.repository.get_by_id(db, comision_id)
        if not comision:
            raise ValueError("Comisión no encontrada.")
        self._validate_scope(db, current_user, comision)
        return comision

    def get_comisiones_tecnico(self, db: Session, tecnico_id: int, current_user):
        if not current_user.is_staff:
            tecnico = db.query(Tecnico).filter(Tecnico.usuario_id == current_user.id).first()
            if not tecnico or tecnico.id != tecnico_id:
                raise PermissionError("No puedes ver comisiones de otros técnicos.")
        return self.repository.get_by_tecnico(db, tecnico_id)

    def get_comisiones_empresa(self, db: Session, empresa_id: int, current_user):
        if not current_user.is_staff and current_user.empresa_id != empresa_id:
            raise PermissionError("No puedes ver comisiones de otras empresas.")
        from models.comision import Comision
        from models.sucursal import Sucursal
        return db.query(Comision).join(Solicitud).join(Sucursal).filter(Sucursal.empresa_id == empresa_id).all()

    def generar_comision(self, db: Session, solicitud_id: int):
        """
        Calcula y guarda la comisión. SOLO debe ejecutarse si la solicitud 
        está finalizada Y el pago está verificado.
        """
        solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
        if not solicitud:
            raise ValueError("Solicitud no encontrada.")
            
        pago = db.query(Pago).filter(Pago.solicitud_id == solicitud_id).first()
        if not pago or pago.estado_pago != EstadoPago.verificado:
            raise ValueError("No se puede generar comisión sin un pago verificado.")
            
        if solicitud.estado != EstadoSolicitud.finalizada:
            raise ValueError("La comisión solo se genera al finalizar la solicitud.")

        existente = self.repository.get_by_solicitud(db, solicitud_id)
        if existente:
            return existente # Ya fue generada

        asig = db.query(Asignacion).filter(
            Asignacion.solicitud_id == solicitud_id, 
            Asignacion.estado == EstadoAsignacion.aceptada
        ).first()
        if not asig:
            raise ValueError("No hay un técnico asignado válido para esta solicitud.")

        monto_base = pago.monto
        porcentaje = 10.0 # Regla de negocio: 10%
        monto_comision_calc = monto_base * (porcentaje / 100.0)

        db_obj = Comision(
            solicitud_id=solicitud_id,
            tecnico_id=asig.tecnico_id,
            pago_id=pago.id,
            monto_base=monto_base,
            porcentaje_comision=porcentaje,
            monto_comision=monto_comision_calc,
            fecha_calculo=datetime.now(timezone.utc),
            observacion="Comisión generada automáticamente por cierre de servicio."
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def marcar_pagada(self, db: Session, comision_id: int, current_user):
        comision = self.get_comision(db, comision_id, current_user)
        return self.repository.update(db, comision_id, {
            "pagado": True, 
            "fecha_pago_comision": datetime.now(timezone.utc),
            "registrado_por_usuario_id": current_user.id
        })
