from sqlalchemy.orm import Session
from schemas.asignacion import AsignacionCreate, AsignacionResponder
from repositories.asignacion_repository import AsignacionRepository
from models.enums import EstadoAsignacion, EstadoSolicitud

class AsignacionService:
    def __init__(self, repository: AsignacionRepository):
        self.repository = repository

    def get_asignaciones(self, db: Session, current_user):
        from models.tecnico import Tecnico
        from models.asignacion import Asignacion
        from models.solicitud import Solicitud
        from models.sucursal import Sucursal
        if current_user.is_staff:
            return db.query(Asignacion).all()
        tecnico = db.query(Tecnico).filter(Tecnico.usuario_id == current_user.id).first()
        if tecnico:
            return self.repository.get_by_tecnico(db, tecnico.id)
        if current_user.empresa_id:
            return (
                db.query(Asignacion)
                .join(Solicitud, Asignacion.solicitud_id == Solicitud.id)
                .join(Sucursal, Solicitud.sucursal_id == Sucursal.id)
                .filter(Sucursal.empresa_id == current_user.empresa_id)
                .all()
            )
        return []

    def get_asignacion(self, db: Session, asignacion_id: int, current_user):
        asignacion = self.repository.get_by_id(db, asignacion_id)
        if not asignacion:
            raise ValueError(f"Asignación {asignacion_id} no encontrada.")
        self._validate_scope(db, current_user, asignacion)
        return asignacion

    def crear_asignacion(self, db: Session, data: AsignacionCreate, current_user):
        from models.tecnico import Tecnico
        from models.usuario import Usuario
        from models.solicitud import Solicitud
        solicitud = db.query(Solicitud).filter(Solicitud.id == data.solicitud_id).first()
        if not solicitud:
            raise ValueError("Solicitud no encontrada.")
        if solicitud.estado != EstadoSolicitud.aceptada.value:
            raise ValueError(
                f"Solo se puede asignar técnico a solicitudes en estado 'aceptada'. "
                f"Estado actual: '{solicitud.estado}'."
            )
        tecnico = db.query(Tecnico).filter(Tecnico.id == data.tecnico_id).first()
        if not tecnico:
            raise ValueError("Técnico no encontrado.")
        if tecnico.estado_operativo != "activo":
            raise ValueError(f"El técnico no está disponible. Estado operativo: '{tecnico.estado_operativo}'.")
        usuario_tecnico = db.query(Usuario).filter(Usuario.id == tecnico.usuario_id).first()
        if not current_user.is_staff and usuario_tecnico.empresa_id != current_user.empresa_id:
            raise PermissionError("Violación de Ámbito: El técnico no pertenece a tu empresa.")
        asignacion = self.repository.create(db, data)
        from repositories.solicitud_repository import SolicitudRepository
        SolicitudRepository().update(db, solicitud.id, {"estado": EstadoSolicitud.tecnico_asignado.value})
        return asignacion

    def responder_asignacion(self, db: Session, asignacion_id: int, data: AsignacionResponder, current_user):
        from models.tecnico import Tecnico
        asignacion = self.repository.get_by_id(db, asignacion_id)
        if not asignacion:
            raise ValueError("Asignación no encontrada.")
        tecnico = db.query(Tecnico).filter(Tecnico.usuario_id == current_user.id).first()
        if not tecnico or tecnico.id != asignacion.tecnico_id:
            raise PermissionError("Solo el técnico asignado puede responder esta asignación.")
        if data.estado not in (EstadoAsignacion.aceptada, EstadoAsignacion.rechazada):
            raise ValueError("Solo se puede aceptar o rechazar una asignación.")
        return self.repository.update(db, asignacion_id, {"estado": data.estado.value})

    def _validate_scope(self, db: Session, current_user, asignacion):
        if current_user.is_staff:
            return
        from models.tecnico import Tecnico
        from models.solicitud import Solicitud
        from models.sucursal import Sucursal
        tecnico = db.query(Tecnico).filter(Tecnico.usuario_id == current_user.id).first()
        if tecnico and tecnico.id == asignacion.tecnico_id:
            return
        solicitud = db.query(Solicitud).filter(Solicitud.id == asignacion.solicitud_id).first()
        if solicitud:
            sucursal = db.query(Sucursal).filter(Sucursal.id == solicitud.sucursal_id).first()
            if sucursal and sucursal.empresa_id == current_user.empresa_id:
                return
        raise PermissionError("Violación de Ámbito: No tienes acceso a esta asignación.")
