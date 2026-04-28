from sqlalchemy.orm import Session
from datetime import datetime, timezone
from schemas.clasificacion_incidente import ClasificacionIncidenteCreate, ClasificacionIncidenteReport, ClasificacionIncidenteRevalidate
from repositories.clasificacion_incidente_repository import ClasificacionIncidenteRepository
from models.solicitud import Solicitud

class ClasificacionIncidenteService:
    def __init__(self, repository: ClasificacionIncidenteRepository):
        self.repository = repository

    def _validate_scope(self, db: Session, current_user, solicitud_id: int):
        if current_user.is_staff:
            return
        sol = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
        if not sol:
            raise ValueError("Solicitud no encontrada.")
        if current_user.type == "cliente" and sol.cliente_id != current_user.id:
             raise PermissionError("No tienes acceso a esta solicitud.")
        # La validación para empresa es más laxa aquí para lectura

    def get_clasificacion(self, db: Session, clasificacion_id: int, current_user):
        clasif = self.repository.get_by_id(db, clasificacion_id)
        if not clasif:
            raise ValueError("Clasificación no encontrada.")
        self._validate_scope(db, current_user, clasif.solicitud_id)
        return clasif

    def get_por_solicitud(self, db: Session, solicitud_id: int, current_user):
        self._validate_scope(db, current_user, solicitud_id)
        return self.repository.get_by_solicitud(db, solicitud_id)

    # Nota: La creación la hace el sistema internamente, pero el service lo permite
    def create_clasificacion(self, db: Session, data: ClasificacionIncidenteCreate):
        # Esta llamada normalmente viene del backend workflow, no expuesta a cliente
        return self.repository.create(db, data)

    def procesar_clasificacion_automatica(self, db: Session, solicitud_id: int):
        """
        Extrae datos de la solicitud y vehculo para alimentar al motor de IA heurstico.
        """
        solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
        if not solicitud: raise ValueError("Solicitud no encontrada.")

        from services.ia_clasificacion_service import IAClasificacionService
        from models.archivo import Archivo
        from models.vehiculo import Vehiculo
        ia_svc = IAClasificacionService()

        # Contexto: Vehculo y Ubicacin
        vehiculo = db.query(Vehiculo).filter(Vehiculo.id == solicitud.vehiculo_id).first()
        contexto = {
            "vehiculo_id": vehiculo.id if vehiculo else None,
            "marca": vehiculo.marca if vehiculo else "desconocida",
            "modelo": vehiculo.modelo if vehiculo else "desconocido",
            "sucursal_id": solicitud.sucursal_id
        }

        # Archivos/Evidencias
        archivos = db.query(Archivo).filter(Archivo.entidad_tipo == "solicitud", Archivo.entidad_id == solicitud_id).all()
        archivos_meta = [{"id": a.id, "mime": a.mime_type} for a in archivos]

        # Clasificar
        resultado_ia = ia_svc.clasificar_incidente(solicitud.descripcion, archivos_meta, contexto)
        
        # Persistir
        data_create = ClasificacionIncidenteCreate(**resultado_ia)
        return self.repository.create(db, data_create)

    def reportar_incorrecta(self, db: Session, clasificacion_id: int, data: ClasificacionIncidenteReport, current_user):
        clasif = self.get_clasificacion(db, clasificacion_id, current_user)
        if clasif.estado_revision != "pendiente":
            raise ValueError("La clasificación ya fue revisada.")
        update_data = {
            "reportada_como_incorrecta": True,
            "motivo_reporte_cliente": data.motivo_reporte_cliente,
            "estado_revision": "cuestionada"
        }
        return self.repository.update(db, clasificacion_id, update_data)

    def revalidar(self, db: Session, clasificacion_id: int, data: ClasificacionIncidenteRevalidate, current_user):
        clasif = self.repository.get_by_id(db, clasificacion_id)
        if not clasif:
            raise ValueError("Clasificación no encontrada.")
        # Debe ser encargado/admin de la empresa
        self._validate_scope(db, current_user, clasif.solicitud_id)
        
        update_data = {
            "estado_revision": data.estado_revision,
            "observacion_revision": data.observacion_revision,
            "revisada_por_usuario_id": current_user.id,
            "fecha_revision": datetime.now(timezone.utc)
        }
        return self.repository.update(db, clasificacion_id, update_data)
