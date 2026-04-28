from sqlalchemy.orm import Session
from schemas.diagnostico import DiagnosticoCreate, DiagnosticoUpdate
from repositories.diagnostico_repository import DiagnosticoRepository

class DiagnosticoService:
    def __init__(self, repository: DiagnosticoRepository):
        self.repository = repository

    def get_diagnostico(self, db: Session, diagnostico_id: int, current_user):
        diagnostico = self.repository.get_by_id(db, diagnostico_id)
        if not diagnostico:
            raise ValueError(f"Diagnóstico {diagnostico_id} no encontrado.")
        self._validate_scope(db, current_user, diagnostico)
        return diagnostico

    def get_por_asignacion(self, db: Session, asignacion_id: int, current_user):
        diagnostico = self.repository.get_by_asignacion(db, asignacion_id)
        if not diagnostico:
            raise ValueError("No existe diagnóstico para esta asignación.")
        self._validate_scope(db, current_user, diagnostico)
        return diagnostico

    def create_diagnostico(self, db: Session, data: DiagnosticoCreate, current_user):
        from models.asignacion import Asignacion
        from models.tecnico import Tecnico
        asignacion = db.query(Asignacion).filter(Asignacion.id == data.asignacion_id).first()
        if not asignacion:
            raise ValueError("Asignación no encontrada.")
        # Solo el técnico de la asignación puede crear el diagnóstico
        tecnico = db.query(Tecnico).filter(Tecnico.usuario_id == current_user.id).first()
        if not current_user.is_staff:
            if not tecnico or tecnico.id != asignacion.tecnico_id:
                raise PermissionError("Solo el técnico de la asignación puede crear el diagnóstico.")
        # 1:1 — no debe existir ya un diagnóstico para esta asignación
        existente = self.repository.get_by_asignacion(db, data.asignacion_id)
        if existente:
            raise ValueError("Ya existe un diagnóstico para esta asignación (relación 1:1).")
            
        # NUEVA REGLA BLOQUE F: Validar que la solicitud tenga un pago verificado ANTES del diagnóstico
        from models.pago import Pago
        pago = db.query(Pago).filter(Pago.solicitud_id == asignacion.solicitud_id).first()
        if not pago or pago.estado_pago != "verificado":
            raise ValueError("No se puede crear el diagnóstico. El pago del servicio debe estar 'verificado' primero.")
            
        return self.repository.create(db, data)

    def update_diagnostico(self, db: Session, diagnostico_id: int, data: DiagnosticoUpdate, current_user):
        diagnostico = self.repository.get_by_id(db, diagnostico_id)
        if not diagnostico:
            raise ValueError("Diagnóstico no encontrado.")
        self._validate_scope(db, current_user, diagnostico)
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, diagnostico_id, clean_update)

    def _validate_scope(self, db: Session, current_user, diagnostico):
        if current_user.is_staff:
            return
        from models.asignacion import Asignacion
        from models.tecnico import Tecnico
        from models.solicitud import Solicitud
        from models.sucursal import Sucursal
        asignacion = db.query(Asignacion).filter(Asignacion.id == diagnostico.asignacion_id).first()
        if not asignacion:
            raise PermissionError("Violación de Ámbito: No se puede verificar acceso al diagnóstico.")
        tecnico = db.query(Tecnico).filter(Tecnico.usuario_id == current_user.id).first()
        if tecnico and tecnico.id == asignacion.tecnico_id:
            return
        if current_user.empresa_id:
            solicitud = db.query(Solicitud).filter(Solicitud.id == asignacion.solicitud_id).first()
            if solicitud:
                sucursal = db.query(Sucursal).filter(Sucursal.id == solicitud.sucursal_id).first()
                if sucursal and sucursal.empresa_id == current_user.empresa_id:
                    return
        raise PermissionError("Violación de Ámbito: No tienes acceso a este diagnóstico.")
