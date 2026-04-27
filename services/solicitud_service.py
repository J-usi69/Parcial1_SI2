from sqlalchemy.orm import Session
from schemas.solicitud import SolicitudCreate, SolicitudUpdate
from repositories.solicitud_repository import SolicitudRepository
from models.enums import EstadoSolicitud
from datetime import datetime, timezone

# Máquina de estados: transiciones válidas
TRANSICIONES_VALIDAS = {
    EstadoSolicitud.pendiente_taller: [EstadoSolicitud.aceptada, EstadoSolicitud.rechazada],
    EstadoSolicitud.aceptada: [EstadoSolicitud.tecnico_asignado, EstadoSolicitud.cancelada],
    EstadoSolicitud.tecnico_asignado: [EstadoSolicitud.en_camino, EstadoSolicitud.cancelada],
    EstadoSolicitud.en_camino: [EstadoSolicitud.punto_encuentro],
    EstadoSolicitud.punto_encuentro: [EstadoSolicitud.trabajo_en_proceso],
    EstadoSolicitud.trabajo_en_proceso: [EstadoSolicitud.finalizada],
    EstadoSolicitud.finalizada: [],
    EstadoSolicitud.rechazada: [],
    EstadoSolicitud.cancelada: [],
}

class SolicitudService:
    def __init__(self, repository: SolicitudRepository):
        self.repository = repository

    def get_solicitudes(self, db: Session, current_user):
        if current_user.is_staff:
            return self.repository.get_all(db)
        # Cliente: solo sus propias solicitudes
        if current_user.type == "cliente":
            return self.repository.get_by_cliente(db, current_user.id)
        # Taller (empresa): solicitudes de su empresa
        if current_user.empresa_id:
            return self.repository.get_by_empresa(db, current_user.empresa_id)
        return []

    def get_solicitud(self, db: Session, solicitud_id: int, current_user):
        solicitud = self.repository.get_by_id(db, solicitud_id)
        if not solicitud:
            raise ValueError(f"Solicitud {solicitud_id} no encontrada.")
        self._validate_scope(db, current_user, solicitud)
        return solicitud

    def create_solicitud(self, db: Session, data: SolicitudCreate, current_user):
        # Cliente solo puede crear para sí mismo
        if current_user.type == "cliente" and data.cliente_id != current_user.id:
            raise PermissionError("Violación de Ámbito: Solo puedes crear solicitudes a tu nombre.")

        # Validar que el servicio_sucursal_id existe y está disponible
        from models.servicio_sucursal import ServicioSucursal
        ss = db.query(ServicioSucursal).filter(
            ServicioSucursal.id == data.servicio_sucursal_id,
            ServicioSucursal.sucursal_id == data.sucursal_id,
            ServicioSucursal.disponible == True
        ).first()
        if not ss:
            raise ValueError(
                "El servicio solicitado no está disponible en la sucursal indicada."
            )
        sol_db = self.repository.create(db, data)

        # REGLA BLOQUE F: Disparar Clasificacion y Recomendacion Automatica (actor: sistema)
        try:
            from services.clasificacion_incidente_service import ClasificacionIncidenteService
            from repositories.clasificacion_incidente_repository import ClasificacionIncidenteRepository
            from services.recomendacion_sucursal_service import RecomendacionSucursalService
            from repositories.recomendacion_sucursal_repository import RecomendacionSucursalRepository

            # 1. Clasificar: extrae contexto real del vehiculo y archivos
            clasif_svc = ClasificacionIncidenteService(ClasificacionIncidenteRepository())
            clasif_svc.procesar_clasificacion_automatica(db, sol_db.id)

            # 2. Recomendar: usa el metodo interno (sin validacion de rol humano)
            recom_svc = RecomendacionSucursalService(RecomendacionSucursalRepository())
            recom_svc._generar_recomendacion_inicial(db, sol_db.id)

        except Exception as e:
            # La IA no debe bloquear la creacion de la solicitud
            print(f"[IA] Error en flujo post-creacion solicitud {sol_db.id}: {str(e)}")

        return sol_db

    def actualizar_estado(self, db: Session, solicitud_id: int, data: SolicitudUpdate, current_user):
        solicitud = self.repository.get_by_id(db, solicitud_id)
        if not solicitud:
            raise ValueError("Solicitud no encontrada.")
        self._validate_scope(db, current_user, solicitud)

        if data.estado:
            estado_actual = EstadoSolicitud(solicitud.estado)
            nuevo_estado = data.estado
            if nuevo_estado not in TRANSICIONES_VALIDAS.get(estado_actual, []):
                raise ValueError(
                    f"Transición inválida: '{estado_actual.value}' → '{nuevo_estado.value}'. "
                    f"Transiciones permitidas: {[e.value for e in TRANSICIONES_VALIDAS[estado_actual]]}"
                )
            # Cerrar solicitud si llega a estado terminal
            if nuevo_estado in (EstadoSolicitud.finalizada, EstadoSolicitud.cancelada, EstadoSolicitud.rechazada):
                data_dict = data.model_dump(exclude_unset=True)
                data_dict["fecha_cierre"] = datetime.now(timezone.utc)
                
                # REGLA BLOQUE F: Generar comisión al finalizar
                if nuevo_estado == EstadoSolicitud.finalizada:
                    from services.comision_service import ComisionService
                    from repositories.comision_repository import ComisionRepository
                    comision_svc = ComisionService(ComisionRepository())
                    comision_svc.generar_comision(db, solicitud_id)

                # REGLA BLOQUE F: Cancelar pagos pendientes si se cancela la solicitud
                if nuevo_estado in (EstadoSolicitud.cancelada, EstadoSolicitud.rechazada):
                    from models.pago import Pago
                    pago_pendiente = db.query(Pago).filter(Pago.solicitud_id == solicitud_id, Pago.estado_pago == "pendiente").first()
                    if pago_pendiente:
                        pago_pendiente.estado_pago = "cancelado"
                        db.commit()

                return self.repository.update(db, solicitud_id, data_dict)

        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, solicitud_id, clean_update)

    def cancelar_solicitud(self, db: Session, solicitud_id: int, motivo: str, current_user):
        solicitud = self.repository.get_by_id(db, solicitud_id)
        if not solicitud:
            raise ValueError("Solicitud no encontrada.")
        self._validate_scope(db, current_user, solicitud)
        estado_actual = EstadoSolicitud(solicitud.estado)
        if EstadoSolicitud.cancelada not in TRANSICIONES_VALIDAS.get(estado_actual, []):
            raise ValueError(f"No se puede cancelar una solicitud en estado '{estado_actual.value}'.")
        # REGLA BLOQUE F: Cancelar pagos pendientes
        from models.pago import Pago
        pago_pendiente = db.query(Pago).filter(Pago.solicitud_id == solicitud_id, Pago.estado_pago == "pendiente").first()
        if pago_pendiente:
            pago_pendiente.estado_pago = "cancelado"
            db.commit()

        return self.repository.update(db, solicitud_id, {
            "estado": EstadoSolicitud.cancelada.value,
            "motivo_cancelacion": motivo,
            "fecha_cierre": datetime.now(timezone.utc)
        })

    def _validate_scope(self, db: Session, current_user, solicitud):
        if current_user.is_staff:
            return
        if current_user.type == "cliente":
            if solicitud.cliente_id != current_user.id:
                raise PermissionError("Violación de Ámbito: No tienes acceso a esta solicitud.")
        elif current_user.empresa_id:
            from models.sucursal import Sucursal
            sucursal = db.query(Sucursal).filter(Sucursal.id == solicitud.sucursal_id).first()
            if not sucursal or sucursal.empresa_id != current_user.empresa_id:
                raise PermissionError("Violación de Ámbito: Esta solicitud no pertenece a tu empresa.")
